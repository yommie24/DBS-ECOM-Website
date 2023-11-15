document.onload = TestProduct();

async function TestProduct() {
    const item = await getItem();
    displayItem(item);

}
async function getItem() {

    // Storing response
    const response = await fetch(window.location.origin + "/items/item/1");

    // Storing data in form of JSON
    const item = await response.json();
    console.log(data);
    return item;
}
function buildItemChild(item) {
    let product = document.createElement("div");
    product.setAttribute("class", "product");
    let name = document.createElement("h1");
    name.innerText = item["name"]
    //             <p>$250</p>
    let price = document.createElement("h2");
    price.innerText = "$" + item["price"]
    desc.appendChild(name);
    desc.appendChild(price);

    return product;

}

function displayItem(item) {
    console.log(item)
    var mainBody = document.getElementById("product");
    item.forEach(item => {
        mainBody.appendChild(
            buildItemChild(item)
        );
    });
}
let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}

