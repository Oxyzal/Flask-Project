const menuIcon = document.querySelector(".hamburger-menu");
const navbar = document.querySelector(".navbar");
menuIcon.addEventListener("click" , function() {
navbar.classList.toggle("change");
} );

const header = document.getElementsByTagName('header')[0]; // We pick up the header or other element we want to change on scroll
const className = 'toggle'; // The name of the class we want to add
const scrollTrigger = 500; // Moment that we want to add class 

document.addEventListener('scroll', function() {
    const top = document.documentElement.scrollTop; // We check at how many pixels we are from the top 
    if (top > scrollTrigger) { // We compare the value we actually have with the one we want 
        header.classList.add(className); // a,d if it's taller than the one we want, we add the class to header
    }else { // and if it's become smaller we removed the class.
        header.classList.remove(className);
    }
});


function seek_range() {
    const capital = document.getElementById('montant')
    const time = document.getElementById('temps')

    capital.addEventListener('input', () => {
        document.getElementById('montant_actuel').innerHTML = ""
        document.getElementById('montant_actuel').innerHTML = capital.value + "€"
    })

    time.addEventListener('input', () => {
        document.getElementById('temps_d').innerHTML = ""
        document.getElementById('temps_d').innerHTML = time.value > 1 ? time.value + " ans" : time.value + " an"
    })
}

seek_range()


document.getElementById("myinput").oninput = function() {
    var value = (this.value-this.min)/(this.max-this.min)*100
    this.style.background = 'linear-gradient(to right, #82CFD0 0%, #82CFD0 ' + value + '%, #fff ' + value + '%, white 100%)'
};



