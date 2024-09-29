/*fra https://www.w3schools.com/howto/howto_js_slideshow.asp*/
let slideIndex = 1;
showSlides(slideIndex);

/* Denne funksjonen viser neste eller forrige bilde */
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
    let slides = document.getElementsByClassName("slide");
    if (n > slides.length) {/* går tilbake til første bilde etter siste bilde */
        slideIndex = 1;
    } 
    if (n < 1) {/* går til siste bilde etter første bilde */
        slideIndex = slides.length;
    }
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = "none"; /* skjuler alle bildene */
    }
    slides[slideIndex-1].style.display = "block"; /* viser det aktuelle bildet */
}


/* Denne funksjonen gjør login validering */
function checkLogin() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    if (email.trim() === '' || password.trim() === '') {
        alert('Vennligst fyll ut både e-post og passord.'); // La til en advarsel hvis feltene er tomme
        return;
    }
    document.getElementById('login_form').submit();
}


/* Denne funksjonen logger inn brukeren */
async function login() {
    let email = document.getElementById("email").value;
    let password = document.getElementById("password").value;
    let form = document.getElementById("login_form");
    form.style.display = "none";

    try {
        let response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
        });
        
        if (!response.ok) {
            form.style.display = "block";
            alert("Feil e-post eller passord!");
            return;
        }

        let user = await response.json(); // La til for å hente brukerdata fra serveren
        document.getElementById("loggedinname").innerText = user.username;
    
    } catch (error) {
        console.log(error);
        alert(`Nettverksfeil: ${error}`);
    }
}


/* Denne funksjonen logger ut brukeren, fra assignment-8 */
async function logout() {
    try {
        let response = await fetch("/logout"); 
        if (response.status != 200) {
            alert("Failed to log out!");
            return;
        }
    } catch (error) {
        console.log(error);
        alert(`Network error: ${error}`);
    }

    let form = document.getElementById("loginform");
    form.style.display = "block";
    let logoutform = document.getElementById("logoutform");
    logoutform.style.display = "none";
}


async function deleteNote() {
    try {
        let url = "/notes/" + note_id;
        let response = await fetch (url, {
            method: "DELETE",
        })
        if (response.status == 200) {
            return true;
        }
        console.log("Error deleting note.")
        } catch (error) {
            console.log(error);
            alert(`Network error: ${error}$`)
        }
        return false
}

/* Søkefunksjon for innlegg */
function searchPosts() {
    let input = document.getElementById('searchBar').value.toLowerCase();
    let posts = document.getElementsByClassName('post');

    for (let i = 0; i < posts.length; i++) {
        let title = posts[i].getAttribute('data-title').toLowerCase();
        let body = posts[i].getAttribute('data-body').toLowerCase();
        let tags = posts[i].getAttribute('data-tags').toLowerCase();
        
        if (title.includes(input) || body.includes(input) || tags.includes(input)) {
            posts[i].style.display = "";
        } else {
            posts[i].style.display = "none";
        }
    }
}


// validering av email i subscribe feltet
function checkEmail() {
    let email = document.getElementById("abonner").value;
    let emailError = document.getElementById("emailError");

    if (email === "" || !email.includes("@")) {
        emailError.textContent = "E-post adressen kan ikke være tom";
        return false; // ikke send inn skjemaet
    } else {
        emailError.textContent = ""; // ingen error
        return true; // send inn skjemaet 
    }
}

/* mobil versjon */
function toggleMenu() {
    let navList = document.querySelector('.nav-list');
    navList.classList.toggle('active');
}
