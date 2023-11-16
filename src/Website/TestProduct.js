fetch('http://127.0.0.1:8000/items/item/1')
  .then(response => response.json())
  .then(data => {

    // Get DOM elements to update 
    const nameSlot = document.getElementById('shoeName');
    const descriptionSlot = document.getElementById('desc');
    const priceSlot = document.getElementById('price')
    
    // Update DOM elements with data
    nameSlot.innerText = data.name; 
    descriptionSlot.innerText = data.description;
    priceSlot.innerText = data.price;

  });
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
