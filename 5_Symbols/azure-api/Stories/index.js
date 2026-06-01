const { BlobServiceClient } = require("@azure/storage-blob");

async function streamToString(readableStream) {
    return new Promise((resolve, reject) => {
        const chunks = [];
        readableStream.on("data", (data) => {
            chunks.push(data.toString());
        });
        readableStream.on("end", () => {
            resolve(chunks.join(""));
        });
        readableStream.on("error", reject);
    });
}

module.exports = async function (context, req) {
    const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    };

    if (req.method === "OPTIONS") {
        context.res = { status: 204, headers: corsHeaders };
        return;
    }

    const connStr = process.env.AzureWebJobsStorage;
    if (!connStr) {
        context.res = { status: 500, headers: corsHeaders, body: { error: "Storage connection not configured" } };
        return;
    }

    try {
        const blobServiceClient = BlobServiceClient.fromConnectionString(connStr);
        const containerClient = blobServiceClient.getContainerClient("stories");
        await containerClient.createIfNotExists();

        // Image upload action — POST /api/stories?action=upload-image
        if (req.method === "POST" && req.query.action === 'upload-image') {
            const { imageData, contentType, username } = req.body || {};
            if (!imageData || !username) {
                context.res = { status: 400, headers: corsHeaders, body: { error: "Missing imageData or username" } };
                return;
            }
            const base64Data = imageData.includes(',') ? imageData.split(',')[1] : imageData;
            const mime = contentType || 'image/png';
            const ext = mime.split('/')[1].replace('jpeg', 'jpg').split('+')[0] || 'png';
            const cleanUsername = username.toLowerCase().replace(/[^a-z0-9]/g, '_');
            const rand = Math.random().toString(36).substr(2, 8);
            const imgFilename = `story-img-${cleanUsername}-${Date.now()}-${rand}.${ext}`;

            const imgContainer = blobServiceClient.getContainerClient("story-images");
            await imgContainer.createIfNotExists({ access: 'blob' });

            const imgBlob = imgContainer.getBlockBlobClient(imgFilename);
            const buf = Buffer.from(base64Data, 'base64');
            await imgBlob.upload(buf, buf.length, {
                blobHTTPHeaders: { blobContentType: mime }
            });

            context.res = {
                status: 200,
                headers: { ...corsHeaders, "Content-Type": "application/json" },
                body: { ok: true, filename: imgFilename, url: imgBlob.url }
            };
            return;
        }

        if (req.method === "GET") {
            const filename = req.query.filename;
            if (filename) {
                if (!filename.match(/^story_[a-z0-9_]+\.json$/)) {
                    context.res = { status: 400, headers: corsHeaders, body: { error: "Invalid filename format" } };
                    return;
                }
                const blockBlobClient = containerClient.getBlockBlobClient(filename);
                const exists = await blockBlobClient.exists();
                if (!exists) {
                    context.res = { status: 404, headers: corsHeaders, body: { error: "Story not found" } };
                    return;
                }
                const downloadResponse = await blockBlobClient.download(0);
                const content = await streamToString(downloadResponse.readableStreamBody);
                context.res = {
                    status: 200,
                    headers: { ...corsHeaders, "Content-Type": "application/json" },
                    body: JSON.parse(content)
                };
                return;
            } else {
                // List all stories with metadata
                const files = [];
                for await (const blob of containerClient.listBlobsFlat({ includeMetadata: true })) {
                    if (blob.name.startsWith('story_') && blob.name.endsWith('.json')) {
                        const displayUsername = blob.metadata && blob.metadata.username
                            ? decodeURIComponent(blob.metadata.username)
                            : blob.name.replace(/^story_/, '').replace(/\.json$/, '');
                        files.push({
                            filename: blob.name,
                            username: displayUsername,
                            lastModified: blob.properties.lastModified
                        });
                    }
                }
                context.res = {
                    status: 200,
                    headers: { ...corsHeaders, "Content-Type": "application/json" },
                    body: { files }
                };
                return;
            }
        }

        if (req.method === "POST") {
            const { username } = req.body;
            if (!username) {
                context.res = { status: 400, headers: corsHeaders, body: { error: "Missing username" } };
                return;
            }
            const cleanUsername = username.toLowerCase().replace(/[^a-z0-9]/g, '_');
            const filename = `story_${cleanUsername}.json`;

            // Deep-copy so we never mutate req.body
            const storyPayload = JSON.parse(JSON.stringify(req.body));

            // Extract any base64 images, upload to story-images container, replace with blob URL
            if (Array.isArray(storyPayload.nodes)) {
                const imgContainer = blobServiceClient.getContainerClient("story-images");
                await imgContainer.createIfNotExists({ access: 'blob' });

                for (const node of storyPayload.nodes) {
                    if (node.image && node.image.startsWith('data:')) {
                        try {
                            const match = node.image.match(/^data:([^;]+);base64,(.+)$/s);
                            if (match) {
                                const contentType = match[1];
                                const ext = contentType.split('/')[1].replace('jpeg', 'jpg').split('+')[0] || 'png';
                                const imgName = `story-img-${cleanUsername}-${Date.now()}-${Math.random().toString(36).substr(2, 6)}.${ext}`;
                                const buf = Buffer.from(match[2], 'base64');
                                const imgBlob = imgContainer.getBlockBlobClient(imgName);
                                await imgBlob.upload(buf, buf.length, {
                                    blobHTTPHeaders: { blobContentType: contentType }
                                });
                                node.image = imgBlob.url;
                                context.log(`[IMG] Uploaded story image → ${imgBlob.url}`);
                            }
                        } catch (imgErr) {
                            context.log.error(`[IMG] Upload failed for node ${node.id}: ${imgErr.message}`);
                            delete node.image; // drop broken base64 rather than store it
                        }
                    }
                }
            }

            const blockBlobClient = containerClient.getBlockBlobClient(filename);
            const content = JSON.stringify(storyPayload);
            await blockBlobClient.upload(content, Buffer.byteLength(content), {
                blobHTTPHeaders: { blobContentType: "application/json" },
                metadata: { username: encodeURIComponent(username) }
            });

            context.res = {
                status: 200,
                headers: { ...corsHeaders, "Content-Type": "application/json" },
                // Return cleaned nodes so the client can sync blob URLs back into local state
                body: { ok: true, filename, url: blockBlobClient.url, nodes: storyPayload.nodes }
            };
            return;
        }

        if (req.method === "DELETE") {
            const filename = req.query.filename || (req.body && req.body.filename);
            if (!filename || !filename.match(/^story_[a-z0-9_]+\.json$/)) {
                context.res = { status: 400, headers: corsHeaders, body: { error: "Invalid or missing filename" } };
                return;
            }
            const sourceBlob = containerClient.getBlockBlobClient(filename);
            const exists = await sourceBlob.exists();
            if (!exists) {
                context.res = { status: 404, headers: corsHeaders, body: { error: "Story not found" } };
                return;
            }

            // Read the content of the source blob
            const downloadResponse = await sourceBlob.download(0);
            const content = await streamToString(downloadResponse.readableStreamBody);
            
            // Get original metadata if any
            const properties = await sourceBlob.getProperties();
            const originalMetadata = properties.metadata || {};

            // Target blob client with _delete_ prefix
            const deleteFilename = `_delete_${filename}`;
            const targetBlob = containerClient.getBlockBlobClient(deleteFilename);
            
            // Upload to target
            await targetBlob.upload(content, Buffer.byteLength(content), {
                blobHTTPHeaders: { blobContentType: "application/json" },
                metadata: originalMetadata
            });

            // Delete original blob
            await sourceBlob.delete();

            context.res = {
                status: 200,
                headers: { ...corsHeaders, "Content-Type": "application/json" },
                body: { ok: true, filename, deleted: true, newFilename: deleteFilename }
            };
            return;
        }

        context.res = { status: 405, headers: corsHeaders, body: { error: "Method Not Allowed" } };
    } catch (err) {
        context.log.error("Stories function error:", err.message);
        context.res = { status: 500, headers: corsHeaders, body: { error: err.message } };
    }
};
