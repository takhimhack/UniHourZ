
if (window.innerWidth < 768) {
	[].slice.call(document.querySelectorAll('[data-bss-disabled-mobile]')).forEach(function (elem) {
		elem.classList.remove('animated');
		elem.removeAttribute('data-bss-hover-animate');
		elem.removeAttribute('data-aos');
	});
}

document.addEventListener('DOMContentLoaded', function() {
	AOS.init();
<<<<<<< HEAD
}, false);

<<<<<<< Updated upstream
const logout = document.querySelector('#logout');
logout.addEventListener('click', (e) => {
	e.preventDefault();
	auth.signout().then(() =>{
		console.log('user has signed out form unihourz')
=======
const uniLogout = document.querySelector('#logout');
uniLogout.addEventListener('click', (e) => {
	e.prevemtDefault();
	auth.signOut().then(()=>{
		console.log('user has logged out');
>>>>>>> Stashed changes
	})
})
=======
}, false);
>>>>>>> 84dce2bb493e4d0641709bcb25afec78e852e18f
