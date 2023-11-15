async function loginUser() {

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const response = await fetch("http://127.0.0.1:8000/token", {
    method: "POST", 
    body: new FormData() {
      append('username', username),
      append('password', password)
    }
  });

  const data = await response.text();

  if (data.includes('access_token')) {
    // successful login
    console.log("Login successful!"); 
  } else {
    // invalid credentials
    console.log("Invalid credentials");
  }

}
