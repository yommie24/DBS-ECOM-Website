async function RegisterUser() {

    const name_f = document.getElementById("name_f").value;
    const name_l = document.getElementById("name_l").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const address = document.getElementById("address").value;
    const contact = document.getElementById("contact").value;


  
    const formData = new FormData();
    formData.append('name_f', name_f);
    formData.append('name_l', name_l);
    formData.append('email', email);
    formData.append('password', password);
    formData.append('address', address);
    formData.append('contact', contact);
  
    const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      body: formData
    }).then(response => {
      if (response.ok) {
          // Login successful - redirect or show message
          alert('Successful Registeration')
          window.location.href = '/static/index.html';
      } else {
          // Login failed - show error 
          alert('Registration failed');
      }
  });
  
    const data = await response.text();
  
    if (data.includes('access_token')) {
      // successful login
      console.log("Registeration successful!");
    } else {   
      // invalid credentials
      console.log("Failed");
    }
    
  
  }
  