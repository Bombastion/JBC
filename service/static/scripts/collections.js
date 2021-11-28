// Functions relating to retrieving and manipulating collections

async function retrieve_collections(client_id) {    
    var collections;

    await jQuery.ajax({
        url: "/get_collections",
        type: "get",
        data: {"client_id": client_id},
        success: function(response) {
            collections = response.collections;
        },
        error: function(response) {
            recent_err = response
            console.log("Failed call to /get_collections: \n" + response.responseJSON.description)
        }
    }); 

    return collections;
}


async function retrieve_items(collection_id) {
    var items;

    await jQuery.ajax({
        url: "/get_items",
        type: "get",
        data: {"collection_id": collection_id},
        success: function(response) {
            items = response.items;
        },
        error: function(response) {
            recent_err = response
            console.log("Failed call to /get_items: \n" + response.responseJSON.description)
        }
    }); 

    return items;
}

async function retrieve_item_types(item_type_id) {
    var item_types;

    await jQuery.ajax({
        url: "/get_item_types",
        type: "get",
        data: {"item_type_id": item_type_id},
        success: function(response) {
            item_types = response.item_types;
        },
        error: function(response) {
            recent_err = response
            console.log(`Failed call to /get_item_types: 
            ${response.responseJSON.description}`);
        }
    }); 

    return item_types;
}