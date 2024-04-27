var sweetAlertScript = document.createElement('script');
sweetAlertScript.src = "https://unpkg.com/sweetalert/dist/sweetalert.min.js";
document.head.appendChild(sweetAlertScript);

// Wait for the script to load
sweetAlertScript.onload = function() {
    $(document).ready(function(){
        // Add to cart
        $('.add_to_cart').on('click', function(e){    
            e.preventDefault();
            var food_id = $(this).data('id');
            var url = $(this).data('url');
            
            $.ajax({
                type: 'GET',
                url: url,
                success: function(response){
                    if(response.status == 'login_required'){
                        swal(response.message, '', 'info').then(function(){
                            window.location = '/login';
                        });
                    } else if(response.status == 'Failed'){
                        swal(response.message, '', 'error');
                    } else {
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        $('#qty-'+food_id).html(response.qty);

                        //total sum when added
                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total']
                        )
                        removeCartItem(response.cartItemQty, cart_id);
                        checkEmptyCart();
                    }
                }
            });
        });

        // Place the cart item quantity on load
        $('.item_qty').each(function(){
            var the_id = $(this).attr('id');
            var qty = $(this).attr('data-qty');
            $('#'+the_id).html(qty);
        });

        // Decrease cart
        $('.decrease_cart').on('click', function(e){
            e.preventDefault();
            
            food_id = $(this).attr('data-id');
            url = $(this).attr('data-url');
            cart_id = $(this).attr('id');
            
            $.ajax({
                type: 'GET',
                url: url,
                success: function(response){
                    if(response.status == 'login_required'){
                        swal(response.message, '', 'info').then(function(){
                            window.location = '/login';
                        });
                    } else if(response.status == 'Failed'){
                        swal(response.message, '', 'error');
                    } else {
                        $('#cart_counter').html(response.cart_counter['cart_count']);
                        $('#qty-'+food_id).html(response.qty);

                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total']
                        )

                        removeCartItem(response.cartItemQty, cart_id);
                        checkEmptyCart();
                    }
                }
            });
        });


        // DELETE CART ITEM
        $('.delete_cart').on('click', function(e){
            e.preventDefault();
            
            var cart_id = $(this).attr('data-id');
            var url = $(this).attr('data-url');
            
            $.ajax({
                type: 'GET',
                url: url,
                success: function(response){
                    console.log(response);
                    if(response.status == 'Success'){  
                        swal(response.message, '', 'success');  
                        $('#cart_counter').html(response.cart_counter['cart_count']);

                        removeCartItem(response.cartItemQty, cart_id);
                        // removeCartItem(0,cart_id);  
                        checkEmptyCart();  
                    } else {
                        swal(response.message, '', 'error');  

                        applyCartAmounts(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total']
                        )

                        removeCartItem(response.cartItemQty, cart_id);
                        checkEmptyCart();
                    } 
                }
            });
        });
      
        //If food_item=0, delete it
        function removeCartItem(cartItemQty,cart_id) {
            if(cartItemQty<=0) {
                document.getElementById("cart-item-"+cart_id).remove()
            }
        }
        // If cart is empty, show "cart is empty" message
        function checkEmptyCart() {
            var cart_counter = document.getElementById("cart_counter").innerHTML;
            if(cart_counter == 0) {
                document.getElementById("empty-cart").style.display = 'block';
            }
        }

        //grandtotal
        function applyCartAmounts(subtotal, tax,grand_total ){
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#grand_total').html(grand_total)

        }



    //     function removeCartItem(cartItemQty, cart_id){
    //         if(cartItemQty <= 0){
    //             // remove the cart item element from html, f.end()
    //             document.getElementById("cart-item-"+cart_id).remove()
    //         }
        
    // }

    // // Check  cart is empty ???
    // function checkEmptyCart(){
    //     var cart_counter = document.getElementById('cart_counter').innerHTML
    //     if(cart_counter == 0){
    //         document.getElementById("empty-cart").style.display = "block";
    //     }
    // }

    });
};




let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {
        types: ['geocode', 'establishment'],
        //default in this app is "IN" - add your country code
        componentRestrictions: {'country': ['in']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }
}

    // get the address components and assign them to the fields
    // console.log(place);
//     var geocoder = new google.maps.Geocoder()
//     var address = document.getElementById('id_address').value

//     geocoder.geocode({'address': address}, function(results, status){
//         // console.log('results=>', results)
//         // console.log('status=>', status)
//         if(status == google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             // console.log('lat=>', latitude);
//             // console.log('long=>', longitude);
//             $('#id_latitude').val(latitude);
//             $('#id_longitude').val(longitude);

//             $('#id_address').val(address);
//         }
//     });

//     // loop through the address components and assign other address data
//     console.log(place.address_components);
//     for(var i=0; i<place.address_components.length; i++){
//         for(var j=0; j<place.address_components[i].types.length; j++){
//             // get country
//             if(place.address_components[i].types[j] == 'country'){
//                 $('#id_country').val(place.address_components[i].long_name);
//             }
//             // get state
//             if(place.address_components[i].types[j] == 'administrative_area_level_1'){
//                 $('#id_state').val(place.address_components[i].long_name);
//             }
//             // get city
//             if(place.address_components[i].types[j] == 'locality'){
//                 $('#id_city').val(place.address_components[i].long_name);
//             }
//             // get pincode
//             if(place.address_components[i].types[j] == 'postal_code'){
//                 $('#id_pin_code').val(place.address_components[i].long_name);
//             }else{
//                 $('#id_pin_code').val("");
//             }
//         }
//     }

// }


// $(document).ready(function(){
//     // add to cart
//     $('.add_to_cart').on('click', function(e){   //class = add_to_cart, in vendordetail.html, 
//         e.preventDefault();                      //and it passes the data-id/ data-url
        
//         food_id = $(this).attr('data-id');
//         url = $(this).attr('data-url');
        
       
//         $.ajax({
//             type: 'GET',    // get the resposne from teh views.
//             url: url,
//             success: function(response){
//                 console.log(response)
//                 if(response.status == 'login_required'){
//                     swal("Login Failed!")
//                     // .then(function(){
//                         // window.location = '/login';
                    
//                 }else if(response.status == 'Failed'){
//                     swal(response.message, '', 'error')
//                 }else{
//                     $('#cart_counter').html(response.cart_counter['cart_count']);
//                     $('#qty-'+food_id).html(response.qty);
//                 }


//                 //     // subtotal, tax and grand total
//                 //     applyCartAmounts(
//                 //         response.cart_amount['subtotal'],
//                 //         response.cart_amount['tax_dict'],
//                 //         response.cart_amount['grand_total']
//                 //     )
//                 // }
//             }
//         })
//     })


//     // place the cart item quantity on load
//     $('.item_qty').each(function(){            //class- item_qty, to calculate the 
//         var the_id = $(this).attr('id')
//         var qty = $(this).attr('data-qty')
//         $('#'+the_id).html(qty)
//     })


