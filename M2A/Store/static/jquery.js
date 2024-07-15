$(function(){

    $(document).ready(function() {
        $('.desc').each(function(){
            if ($(this).text().length > 220){
                var desc = $(this).text();
                desc = desc.substring(0,220)
                desc = desc.split(" ");
                desc.pop()
                desc = desc.join(" ") + " ...";
                $(this).text(desc);
            };
        })   
    });

    $(document).ready(function() {
        $('.descripcionportada').each(function(){
            if ($(this).text().length > 100){
                var desc = $(this).text();
                desc = desc.substring(0,100)
                desc = desc.split(" ");
                desc.pop()
                desc = desc.join(" ") + " ...";
                $(this).text(desc);
            };
        })   
    });

//conversión a dólares
    $(document).ready(function() {$('.spinner-border').hide();});
    $('.btnConversion').click(function(){
        $('.precioJuego').hide();
        $('.spinner-border').show();
        $.getJSON('https://mindicador.cl/api', function(data) {
            if ($('.btnConversion').text().trim() == "Convertir a dólares"){
                var dolar = data.dolar.valor;
                var precio = $('.precioJuego').text().substring(1, $('.precioJuego').text().length-4).replaceAll('.', '');
                var precioDolarizado = Math.round((precio / dolar)*100) / 100; //dos decimales
                $('.precioJuegoConvertido').text("$"+ precioDolarizado + " USD");
                $('.spinner-border').hide();
                $('.precioJuegoConvertido').show();
                $('.btnConversion').text("Convertir a pesos");
            }
            else if ($('.btnConversion').text().trim() == "Convertir a pesos"){
                $('.spinner-border').hide();
                $('.precioJuego').show();
                $('.precioJuegoConvertido').hide();
                $('.btnConversion').text("Convertir a dólares"); 
            }
        }).fail(function() {
    console.log('Error al consumir la API!');
        })
    })

    //imágenes API
    Fancybox.bind('[data-fancybox="galeria1"]', {
      });
    Fancybox.bind('[data-fancybox="galeria2"]', { 
      });
    Fancybox.bind('[data-fancybox="galeria3"]', {
      });
    Fancybox.bind('[data-fancybox="galeria4"]', { 
      });
    Fancybox.bind('[data-fancybox="galeria5"]', {
      });
    Fancybox.bind('[data-fancybox="galeria6"]', { 
      });
    Fancybox.bind('[data-fancybox="galeria7"]', {
      });

// calcular subtotal
    $(document).ready($(function() {
        var suma = 0
        $('#carro tr').each(function() {
            if(parseFloat($(this).find('.cantidad').val()) && parseFloat($(this).find('.precio-carro').text())){
                var cantidad = $(this).find('.cantidad').val();
                var precio = $(this).find('.precio-carro').text();
                var subtotal = Math.trunc(cantidad * precio);
                $(this).find('.subtotal').text(subtotal);
                suma+=subtotal
            }        
        });
        $('#subtotal').text(suma);
    }));

    $(":input").bind('keyup mouseup', function () {
        var suma = 0
        $('#carro tr').each(function() {
            if(parseFloat($(this).find('.cantidad').val()) && parseFloat($(this).find('.precio-carro').text())){
                var cantidad = $(this).find('.cantidad').val();
                var precio = $(this).find('.precio-carro').text();
                var subtotal = Math.trunc(cantidad * precio);
                $(this).find('.subtotal').text(subtotal);
                suma+=subtotal
            }        
        });
        $('#subtotal').text(suma);           
    });

//total
    $(document).ready($(function() {
        var total = Math.round(parseFloat($('#subtotal').text())*1.19);
        //$('#total').text(Math.round(parseFloat($('#subtotal').text())*1.19));
        $('.total').val(total);
    }));

    // $(":input").bind('keyup mouseup', function () {
    //     $('#total').text(Math.round(parseFloat($('#subtotal').text())*1.19));
    // });


//vista previa
    // $('#enviarSerie').click(function(){
    //     if (!($('.txtSImg').val() == '')){
    //         var fileInput = $('.txtSImg')[0];
    //         var file = fileInput.files[0];
    //         var url = URL.createObjectURL(file);
    //         $('.vista-previa').attr('src', url);
    //     }
    // })

    $('.btnVistaPreviaS').click(function(){
        if (!($('.Img').val() == '')){
            var fileInput = $('.Img')[0];
            var file = fileInput.files[0];
            var url = URL.createObjectURL(file);
            $('.vista-previa').attr('src', url);
        }
    })

    $('.btnVistaPreviaJ').click(function(){
        if (!($('.Img').val() == '')){
            var fileInput = $('.Img')[0];
            var file = fileInput.files[0];
            var url = URL.createObjectURL(file);
            $('.vista-previa').attr('src', url);
        }
    })

    //$('#enviarJuego').click(function(){
        //if (!($('.txtJImg').val() == '')){
          //  var fileInput = $('.txtJImg')[0];
         //   var file = fileInput.files[0];
         //   var url = URL.createObjectURL(file);
         //   $('.vista-previa').attr('src', url);
       // }
   // })

    //verificaciones 

    //rut test
    function verificarRUT(rut){
        var suma = 0
        var mult = 2;
        var run = rut.substring(0,8);
        run = run.split('').reverse();
        $.each(run, function(index, dig){
         suma+=dig*mult;
         mult+=1;
         if(mult==8){mult=2};
      })
      var div=suma/11
      var result=11-Math.abs(suma-Math.trunc(div)*11)
      if(result==11){return '0'} else if(result==10){return 'K'}
      else return result;
      };
          
      $('#enviarRegistro').click(function(){
        $('input,select').each(function() {
            $(this)[0].setCustomValidity('');
        });
       var rut = $.trim($('.txtRut').val());
       if($.trim($('.txtRut').val())==""){
        $('.txtRut')[0].setCustomValidity('Ingrese un RUT válido.')
        $('.txtRut').focus();
       }
       else if(!(/^\d{8}-[\dk]{1}$/.test(rut))){
        $('.txtRut')[0].setCustomValidity('Ingrese un RUT válido.')
        $('.txtRut').focus();
       }
       else if(verificarRUT(rut)!=rut.substring(9,10)){
        $('.txtRut')[0].setCustomValidity('Ingrese un RUT válido.')
        $('.txtRut').focus();
       }   
       else if($.trim($('.txtNombre').val())==""){
        $('.txtNombre')[0].setCustomValidity('Ingrese un nombre.');
        $('.txtNombre').focus();
       }
       else if($.trim($('.txtNombre').val()).length>=35){
        $('.txtNombre')[0].setCustomValidity('El nombre excede el máximo de caracteres (35).')
        $('.txtNombre').focus();
       }
       else if($.trim($('.txtApellido').val())==""){
        $('.txtApellido')[0].setCustomValidity('Ingrese un apellido.');
        $('.txtApellido').focus();
       }
       else if($.trim($('.txtApellido').val()).length>=35){
        $('.txtApellido')[0].setCustomValidity('El apellido excede el máximo de caracteres (35).')
        $('.txtApellido').focus();
       }
       else if($.trim($('.txtEmail').val())==""){
        $('.txtEmail')[0].setCustomValidity('Ingrese un email valido.');
        $('.txtEmail').focus();
       }
       else if(!(/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test($.trim($('.txtEmail').val())))){
        $('.txtEmail')[0].setCustomValidity('Ingrese un email valido.');
        $('.txtEmail').focus();
       }
       else if($.trim($('.txtEmail').val()).length>=70){
        $('.txtEmail')[0].setCustomValidity('El email excede el máximo de caracteres (70).')
        $('.txtEmail').focus();
       }
       else if($.trim($('.txtTelefono').val())==""){
        $('.txtTelefono')[0].setCustomValidity('Ingrese teléfono válido.');
        $('.txtTelefono').focus();
       }
       else if(!(/^[\+]{1}(569|562)[\d]{8}$/.test($.trim($('.txtTelefono').val())))) {
        $('.txtTelefono')[0].setCustomValidity('Debe empezar con +569/+562, 8 digitos.');
        $('.txtTelefono').focus();
        }
       else if($.trim($('.selectRegion').val())=="Seleccionar Región"){
        $('.selectRegion')[0].setCustomValidity('Seleccione una región.');
        $('.selectRegion').focus();
       }
       else if($.trim($('.selectRegion').val())==""){
        $('.selectRegion')[0].setCustomValidity('Seleccione una región.');
        $('.selectRegion').focus();
       }
       else if($.trim($('.selectNac').val())==""){
        $('.selectNac')[0].setCustomValidity("Seleccione fecha de nacimiento.");
        $('.selectNac').focus();
       }
       else if($.trim($('.selectEd').val())=="Seleccionar"){
        $('.selectEd')[0].setCustomValidity("Seleccione un nivel educacional.");
        $('.selectEd').focus();
       }
       else if($.trim($('.selectEd').val())==""){
        $('.selectEd')[0].setCustomValidity("Seleccione un nivel educacional.");
        $('.selectEd').focus();
       }
    });

    $('.txtRut, .txtNombre, .txtApellido, .txtEmail, .txtTelefono, .selectRegion, .selectEd, .selectNac').on('keyup', function() {
        $(this).get(0).setCustomValidity('');
    });
    
    $('#limpiarRegistro').click(function(){
        $('input,select').each(function() {
            $(this).val('');
        });
    })

    $('#limpiarSerie').click(function(){
        $('.txtSTitulo').val('');
        $('.txtSDesc').val('');
        $('.txtSImg').val('');
        $('.txtLink').val('');
        $('.txtSKeys').val('');
        $('.txtSCategoria').val('');
        $('.txtSEstudio').val('');
        $('.txtSFecha').val('');
        $('.txtSPrecio').val('');
        $('.txtSStock').val('');
        $('.vista-previa').attr('src', 'img/placeholder.png');
    })

    $('#limpiarJuego').click(function(){
        $('.txtJNombre').val('');
        $('.txtJDev').val('');
        $('.txtJDesc').val('');
        $('.txtJImg').val('');
        $('.txtJPrecio').val('');
        $('.txtJStock').val('');
        $('.txtJKeys').val('');
        $('.txtLink').val('');
        $('.txtJPlataforma').val('');
        $('.vista-previa').attr('src', 'img/placeholder.png');
    })

    $('#enviarSerie').click(function(){
        $('.txtSTitulo, .txtSDesc, .txtSImg, .txtSKeys, .txtSPrecio, .txtSStock, .txtSCategoria, .txtSFecha').each(function() {
            this.setCustomValidity('');

        });
        if($.trim($('.txtSTitulo').val())==""){
            $('.txtSTitulo')[0].setCustomValidity('Ingrese un título.')
            $('.txtSTitulo').focus();
        }
        else if($.trim($('.txtSTitulo').val()).length>=20){
            $('.txtSTitulo')[0].setCustomValidity('Titulo no puede tener más de 20 caracteres.')
            $('.txtSTitulo').focus();
        }
        else if($.trim($('.txtSEstudio').val())==""){
            $('.txtSEstudio')[0].setCustomValidity('Ingrese un estudio')
            $('.txtSEstudio').focus();
        }
        else if($.trim($('.txtSDesc').val())==""){
            $('.txtSDesc')[0].setCustomValidity('Ingrese una descripción.')
            $('.txtSDesc').focus();
        }
        else if($.trim($('.txtSImg').val())==""){
            $('.txtSImg')[0].setCustomValidity('Seleccione una imagen.')
            $('.txtSImg').focus();
        }
        else if($.trim($('.txtSKeys').val())==""){
            $('.txtSKeys')[0].setCustomValidity('Seleccione un archivo con claves.')
            $('.txtSKeys').focus();
        }
        else if($.trim($('.txtSPrecio').val())==""){
            $('.txtSPrecio')[0].setCustomValidity('Ingrese precio unitario.')
            $('.txtSPrecio').focus();
        }
        else if($.trim($('.txtSPrecio').val())<=0){
            $('.txtSPrecio')[0].setCustomValidity('Precio no puede ser 0 o menos')
            $('.txtSPrecio').focus();
        }
        else if($.trim($('.txtSStock').val())==""){
            $('.txtSStock')[0].setCustomValidity('Ingrese cantidad de stock disponible.')
            $('.txtSStock').focus();
        }
        else if($.trim($('.txtSCategoria').val())==""){
            $('.txtSCategoria')[0].setCustomValidity('Seleccione una categoría.')
            $('.txtSCategoria').focus();
        }
        else if($.trim($('.txtSFecha').val())==""){
            $('.txtSFecha')[0].setCustomValidity('Seleccione una fecha de lanzamiento.')
            $('.txtSFecha').focus();
        }
        else{
            alert("Serie agregada con éxito.")
        }
    })

    $('.txtSTitulo, .txtSDesc, .txtSImg, .txtSKeys, .txtSPrecio, .txtSStock, .txtSCategoria, .txtSFecha').on('keyup', function() {
        $(this).get(0).setCustomValidity('');
    });



    $('#enviarJuego').click(function(){
        $('.txtJNombre, .txtJDev, .txtJDesc, .txtJImg, .txtLink, .txtJPrecio, .txtJStock, .txtJKeys, .txtJPlataforma').each(function() {
            this.setCustomValidity('');
        });

        if($.trim($('.txtJNombre').val())==""){
            $('.txtJNombre')[0].setCustomValidity('Ingrese un titulo.');
            $('.txtJNombre').focus();
           }
        else if($.trim($('.txtJNombre').val()).length>=20){
            $('.txtJNombre')[0].setCustomValidity('El título no puede tener más de 20 carácteres');
            $('.txtJNombre').focus();
        }
        else if($.trim($('.txtJDev').val())==""){
            $('.txtJDev')[0].setCustomValidity('Ingrese un desarrollador.');
            $('.txtJDev').focus();
        }
        else if($.trim($('.txtJDesc').val())==""){
            $('.txtJDesc')[0].setCustomValidity('Ingrese una descripción del juego.');
            $('.txtJDesc').focus();
        }
        else if($.trim($('.txtJDesc').val()).length>=520){
            $('.txtJNombre')[0].setCustomValidity('Límite de 520 carácteres.');
            $('.txtJNombre').focus();
        }
        //else if($.trim($('.txtJImg').val())==""){
          //  $('.txtJImg')[0].setCustomValidity('Ingrese una imagen.');
          //  $('.txtJImg').focus();
      //  }
        else if($.trim($('.txtJPrecio').val())==""){
            $('.txtJPrecio')[0].setCustomValidity('Ingrese un precio unitario.');
            $('.txtJPrecio').focus();
        }
        else if($.trim($('.txtJPrecio').val())<=0){
            $('.txtJPrecio')[0].setCustomValidity('Precio no puede ser 0 o menos.');
            $('.txtJPrecio').focus();
        }
        else if($.trim($('.txtJStock').val())==""){
            $('.txtJStock')[0].setCustomValidity('Debe ingresar stock disponible.');
            $('.txtJStock').focus();
        }
       // else if($.trim($('.txtJKeys').val())==""){
          //  $('.txtJKeys')[0].setCustomValidity('Debe adjuntar las keys, formato ZIP y RAR.');
          //  $('.txtJKeys').focus();
            
        //}
        else if($.trim($('.txtLink').val())==""){
            $('.txtLink')[0].setCustomValidity('Debe ingresar el link de youtube.');
            $('.txtLink').focus();
            
        }
        //else if($.trim($('.txtLink').val()).length!=43){
          //  $('.txtLink')[0].setCustomValidity('Link inválido');
            //$('.txtLink').focus();
        //}
        else if($.trim($('.txtJPlataforma').val())==""){
            $('.txtJPlataforma')[0].setCustomValidity('Ingrese plataforma.');
            $('.txtJPlataforma').focus();
        }
        else{
            console.log("formulario correcto")
        }
        
    });
    $('.txtJNombre, .txtJDev, .txtJDesc, .txtJImg, .txtJPrecio, .txtJStock, .txtJKeys, .txtJPlataforma').on('keyup', function() {
        $(this).get(0).setCustomValidity('');
    });
    
});