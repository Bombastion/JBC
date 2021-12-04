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

async function add_item_type(name,
                             producer) {
    var new_item_type;

    await jQuery.ajax({
        url: "/add_new_item_type",
        type: "post",
        data: {
            "new_item_type_name": name,
            "new_item_type_producer": producer,
        },
        success: function(response) {
            new_item_type = response; 
        },
        error: function(response) {
            recent_err = response
            console.log(`Failed call to /add_new_item_type: 
            ${response.responseJSON.description}`);
        }
    });

    return new_item_type;
}   

async function add_collection_for_user(client_id,
                                       collection_name) {
    var new_collection;

    await jQuery.ajax({
        url: "/add_new_collection",
        type: "post",
        data: {
            "client_id": client_id,
            "new_collection_name": collection_name,
        },
        success: function(response) {
            new_collection = response; 
        },
        error: function(response) {
            recent_err = response
            console.log(`Failed call to /add_new_collection: 
            ${response.responseJSON.description}`);
        }
    });

    return new_collection;
}   

async function add_item_to_collection(item_type_id,
                                      collection_id,
                                      amount) {
    var new_item;

    await jQuery.ajax({
        url: "/add_item_to_collection",
        type: "post",
        data: {
            "item_type_id": item_type_id,
            "collection_id": collection_id,
            "quantity": amount
        },
        success: function(response) {
            new_item = response; 
        },
        error: function(response) {
            recent_err = response
            console.log(`Failed call to /add_item_to_collection: 
            ${response.responseJSON.description}`);
        }
    });

    return new_item;
}

async function modify_item(item_id,
                           new_quantity) {
    var modified_item;

    await jQuery.ajax({
        url: "/modify_item",
        type: "post",
        data: {
            "item_id": item_id,
            "new_quantity": new_quantity,
        },
        success: function(response) {
            modified_item = response; 
        },
        error: function(response) {
            recent_err = response
            console.log(`Failed call to /modify_item: 
            ${response.responseJSON.description}`);
        }
    });

    return modified_item;
}