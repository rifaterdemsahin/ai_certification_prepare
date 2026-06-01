const { BlobServiceClient } = require("@azure/storage-blob");

module.exports = async function (context, req) {
    const corsHeaders = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type"
    };

    if (req.method === "OPTIONS") {
        context.res = { status: 204, headers: corsHeaders };
        return;
    }

    if (req.method !== "POST") {
        context.res = { status: 405, headers: corsHeaders, body: { error: "Method Not Allowed" } };
        return;
    }

    const connStr = process.env.AzureWebJobsStorage;
    if (!connStr) {
        context.res = { status: 500, headers: corsHeaders, body: { error: "Storage connection not configured" } };
        return;
    }

    try {
        const { imageData, contentType, username } = req.body || {};
        if (!imageData || !username) {
            context.res = { status: 400, headers: corsHeaders, body: { error: "Missing imageData or username" } };
            return;
        }

        // Strip data URL prefix (data:image/png;base64,<data>)
        const base64Data = imageData.includes(',') ? imageData.split(',')[1] : imageData;
        const mime = contentType || 'image/png';
        const ext = mime.split('/')[1].replace('jpeg', 'jpg').split('+')[0] || 'png';
        const cleanUsername = (username || 'anon').toLowerCase().replace(/[^a-z0-9]/g, '_');
        const filename = `story-img-${cleanUsername}-${Date.now()}.${ext}`;

        const blobServiceClient = BlobServiceClient.fromConnectionString(connStr);
        const containerClient = blobServiceClient.getContainerClient("story-images");
        await containerClient.createIfNotExists({ access: 'blob' });

        const blockBlobClient = containerClient.getBlockBlobClient(filename);
        const buffer = Buffer.from(base64Data, 'base64');
        await blockBlobClient.upload(buffer, buffer.length, {
            blobHTTPHeaders: { blobContentType: mime }
        });

        context.res = {
            status: 200,
            headers: { ...corsHeaders, "Content-Type": "application/json" },
            body: { ok: true, filename, url: blockBlobClient.url }
        };
    } catch (err) {
        context.log.error("StoryImages error:", err.message);
        context.res = { status: 500, headers: corsHeaders, body: { error: err.message } };
    }
};
