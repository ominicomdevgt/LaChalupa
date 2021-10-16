 $(document).ready(function() {
         
            $.cookit({
  messageText: "Utilizamos cookies solo para recoger estadísticas de uso sin almacenar datos personales.",
  linkText: "Política de cookies",
  linkUrl: "#",
  buttonText: "ACEPTO"
});

setTimeout(function(){
    $('#cookit').hide();
}, 30000);
            $("a").on('click', function(event) {
                if (this.hash !== "") {

                    event.preventDefault();
                    var hash = this.hash;

                    $('html, body').animate({
                        scrollTop: $(hash).offset().top-90
                    }, 300, function() {

                        window.location.hash = hash;
                    });
                } // End if
            });
        });
