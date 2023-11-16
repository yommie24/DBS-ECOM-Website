async function loginUser() {

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);

  const response = await fetch("http://127.0.0.1:8000/token", {
    method: "POST",
    body: formData
  }).then(response => {
    if (response.ok) {
        // Login successful - redirect or show message
        alert('Successful login')
        document.cookie = `username=${username}`;
        window.location.href = '/static/index.html';
    } else {
        // Login failed - show error 
        alert('Invalid email or password');
    }
});

  const data = await response.text();

  if (data.includes('access_token')) {
    document.cookie = `username=${access_token}`;
    console.log("Login successful!");
  } else {   
    // invalid credentials
    console.log("Invalid credentials");
  }
  

}

