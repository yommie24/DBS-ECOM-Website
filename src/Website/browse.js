// const menu = document.querySelector(".menu");
// const menuBtn = document.querySelector(".menu-btn");

// menuBtn.addEventListener("click", () => {
//     menu.classList.toggle('nav-toggle');
// });

document.onload = browse();

async function browse() {
    const shoes = await getShoes();
    displayShoes(shoes);

}

async function getShoes() {
    const response = await fetch(window.location.origin + "/items/all");
    const shoes = await response.json();
    return shoes;
}

function buildShoeChild(shoe) {
    // <div class="product">
    let product = document.createElement("div");
    product.setAttribute("class", "product");

    
    //         <img src="https://i.ibb.co/TWwhx3K/eef10c9cfc937ea3fcd0a62d018cd21d-removebg-preview.png" width="200px" height="200px">
    let thumb = document.createElement("img");
    thumb.src = shoe.thumbnail;


    //         <div class="product_desc">
    let desc = document.createElement("div");
    
    desc.setAttribute("class", "product_desc");
    //             <h3>Jordan 1</h3>
    let name = document.createElement("h3");
    name.innerText = shoe["name"]
    //             <p>$250</p>
    let price = document.createElement("p");
    price.innerText = "$" + shoe["price"]

    let button = document.createElement("button");
    button.innerText = "View Details";

    desc.appendChild(name);
    desc.appendChild(price);
    desc.appendChild(button);
    
    

    let rating = document.createElement("div")
    rating.setAttribute("class", "rating");
    //                 <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    //                 <span class ="fa fa-star checked"></span>
    //                 <span class ="fa fa-star checked"></span>
    //                 <span class ="fa fa-star checked"></span>
    //                 <span class ="fa fa-star checked"></span>
    //                 <span class ="fa fa-star"></span>
    //             </div>

    //         </div>
    product.appendChild(thumb);
    product.appendChild(desc);
    //     </div>


    return product;
}

function displayShoes(shoes) {
    console.log(shoes)
    var mainBody = document.getElementById("main_container");
    shoes.forEach(shoe => {
        mainBody.appendChild(
            buildShoeChild(shoe)
        );
    });
}
