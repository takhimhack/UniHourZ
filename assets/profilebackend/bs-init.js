
if (window.innerWidth < 768) {
	[].slice.call(document.querySelectorAll('[data-bss-disabled-mobile]')).forEach(function (elem) {
		elem.classList.remove('animated');
		elem.removeAttribute('data-bss-hover-animate');
		elem.removeAttribute('data-aos');
	});
}

document.addEventListener('DOMContentLoaded', function() {
	AOS.init();
}, false);

const logout = document.getElementById('logout');
logout.addEventListener('click', (e) => {
	e.preventDefault();
	auth.signOut().then(() =>{
		console.log('user has signed out form unihourz')
	})
	var href = "index.html";
	window.location=href;	
})