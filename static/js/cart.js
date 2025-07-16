// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    var updateBtns = document.getElementsByClassName("update-cart");
    var removeButtons = document.getElementsByClassName('remove-item');
    
    console.log("Found", updateBtns.length, "update buttons");
    console.log("Found", removeButtons.length, "remove buttons");

    // Handle update cart buttons (add/remove quantity)
    for (var i = 0; i < updateBtns.length; i++) {
        updateBtns[i].addEventListener("click", function () {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log("Update button clicked - productId:", productId, "Action:", action);
            console.log("USER:", user);

            if (user == "AnonymousUser") {
                addCookieItem(productId, action);
            } else {
                updateUserOrder(productId, action);
            }
        });
    }

    // Handle remove item buttons (complete removal)
    for (var i = 0; i < removeButtons.length; i++) {
        removeButtons[i].addEventListener("click", function () {
            var productId = this.dataset.product;
            var action = this.dataset.action;
            console.log("Remove button clicked - productId:", productId, "Action:", action);
            console.log("USER:", user);

            if (confirm('Are you sure you want to remove this item from your cart?')) {
                if (user == "AnonymousUser") {
                    addCookieItem(productId, action);
                } else {
                    updateUserOrder(productId, action);
                }
            }
        });
    }
});

function updateUserOrder(productId, action) {
    console.log("User is authenticated, sending data...");
    console.log("Sending:", {productId: productId, action: action});

    var url = "/update_item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
    .then((response) => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log("Response data:", data);
        location.reload();
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('An error occurred while updating the cart. Please try again.');
    });
}

function addCookieItem(productId, action) {
    console.log("User is not authenticated, updating cookie cart");
    console.log("Current cart:", cart);

    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { quantity: 1 };
        } else {
            cart[productId]["quantity"] += 1;
        }
    }

    if (action == "remove") {
        if (cart[productId] != undefined) {
            cart[productId]["quantity"] -= 1;

            if (cart[productId]["quantity"] <= 0) {
                console.log("Item should be deleted");
                delete cart[productId];
            }
        }
    }

    if (action == "delete") {
        console.log("Removing item completely from cart");
        delete cart[productId];
    }

    console.log("Updated cart:", cart);
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/";
    location.reload();
}