// counter function for Visitor counter
const { TableClient, AzureNamedKeyCredential } = require("@azure/data-tables");

const tableName = "VisitorCounter";
const accountName = process.env.TABLE_ACCOUNT_NAME;
const accountKey = process.env.TABLE_ACCOUNT_KEY;

const credential = new AzureNamedKeyCredential(accountName, accountKey);
const client = new TableClient(`https://${accountName}.table.core.windows.net`, tableName, credential);

module.exports = async function (context, req) {
    const partitionKey = "visitor";
    const rowKey = "count";

    // Try to get existing count
    let entity;
    try {
        entity = await client.getEntity(partitionKey, rowKey);
        entity.value++;
        await client.updateEntity(entity, "Merge");
    } catch {
        entity = { partitionKey, rowKey, value: 1 };
        await client.createEntity(entity);
    }

    context.res = {
        status: 200,
        body: entity.value.toString()
    };
};
