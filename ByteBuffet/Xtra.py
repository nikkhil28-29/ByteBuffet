
# from datetime import time

# t = [(time(h, m).strftime("%I:%M %p"), time(h, m).strftime("%I:%M %p")) for h in range(0, 24) for m in range(0, 60, 30)]
# print(t)

        



# # Code header.html
# {% load static %}
# {% comment %} {% extends 'base.html' %}   {% endcomment %}




#     <div class="wrapper">
# <!-- Header Start -->
#         # <header id="header">
#             <div class="main-header">
#                 <div class="container-fluid">
#                     <div class="row">
#                         <div class="col-lg-8 col-md-8 col-sm-12 col-xs-12">
#                             <div class="logo">
#                                 <figure>
#                                     <a href="{% url 'home' %}" class="light-logo">
#                                         <img src="{% static 'logo/ByteBasket.png' %}" alt="FoodBakery" width="150" height="150">
#                                     </a>
#                                 </figure>
#                             </div>
#                             <div class="main-nav">
#                                     <nav id="site-navigation" class="main-navigation">
#                                         <ul>
#                                             <li>
#                                                 <a href="#">Demos</a>
#                                                 <ul>
#                                                     <li><a href="index.html">Food Bakery</a></li>
#                                                     <li><a href="mexican-restaurant.html">Mexican Restaurant</a></li>
#                                                     <li><a href="foodstop.html">Food Stop</a></li>
#                                                     <li><a href="rtl.html">Rtl Demo</a></li>
#                                                     <li><a href="food-cout.html">Food Court</a></li>
#                                                     <li><a href="single-restaurant.html">Single Restaurant Demo</a></li>
#                                                 </ul>
#                                                 <!--End Sub Menu -->
#                                             </li>
#                                             <li><a href="listings.html">Restaurants</a></li>
#                                             <li>
#                                                 <a href="#">Pages</a>
#                                                 <ul>
#                                                     <li><a href="price-plans.html">Price Plans</a></li>
#                                                     <li><a href="how-it-works.html">How it works</a></li>
#                                                     <li><a href="faq.html">FAQ’s</a></li>
#                                                     <li><a href="404.html">404</a></li>
#                                                     <li><a href="search-result.html">Search Result</a></li>
#                                                     <li><a href="contact-us.html">Contact</a></li>
#                                                 </ul>
#                                                 <!--End Sub Menu -->
#                                             </li>
#                                             <li>
#                                                 <a href="#">Blogs</a>
#                                                 <ul>
#                                                     <li><a href="blog-large.html">Blog Large</a></li>
#                                                     <li><a href="blog-medium.html">Blog Medium</a></li>
#                                                     <li><a href="blog-masonry.html">Blog Masonry</a></li>
#                                                     <li><a href="blog-detail.html">Blog Detail Page</a></li>
#                                                 </ul>
#                                                 <!--End Sub Menu -->
#                                             </li>
#                                         </ul>
#                                     </nav><!-- .main-navigation -->
#                                 </div>
                           
#                             <div class="main-location">
#                                 <ul>
#                                     <li class="location-has-children choose-location">
#                                         <form action="#">
#                                             <input type="text" value="" name="location" placeholder="Enter your delivery location" autocomplete="off">
#                                             <span id="foodbakery_radius_location_open" class="foodbakery-radius-location"><i class="icon-target5"></i></span>
#                                         </form>
                                       
#                                     </li>
#                                 </ul>
#                                 </div>
#                         </div>
#                         <div class="col-lg-4 col-md-4 col-sm-12 col-xs-12">
#                         <div class="login-option">
#                         {% if user.is_authenticated %}
#                             <a href="{% url 'cart' %}">
#                                 <i class="fas fa-shopping-cart text-danger" style="font-size: 20px;"></i>
#                                 <span class="badge badge-warning" id="cart_counter" style="border-radius: 50px; position: relative; bottom:10px; left: -5px;">{{ cart_count }}</span>
#                             </a>
#                             {% endif %}


#                         <a href="{% url 'marketplace' %}" class="btn  text-uppercase bold" style="background-color: #3498db; color: black; font-weight: bold;">MarketPlace </a>




#                         {% if user.is_authenticated %}
#                             <span><a href="{% url 'logout' %}" class="get-start-btn" style="background-color: #FFFF00;">Logout</a></span>
#                             <span><a href="{% url 'myAccount' %}" class="get-start-btn" style="background-color: #00FF00;">myAccount</a></span>
#                         {% else %}
#                             <span><a href="{% url 'login' %}" class="get-start-btn" style="background-color: #FFFF00;">Login</a></span>
#                             <span><a href="{% url 'registerUser' %}" class="cs-color cs-popup-joinus-btn login-popup ml-0">Register</a></span>
                       
#                         <a class="get-start-btn" href="{% url 'registerVendor' %}">Register Restaurant</a>
#                         {% endif %}
#                     </div>
#                 </div>


#                     </div>
#                 </div>
#             </div>
#         </header>
#         <!-- Header End -->
#     </div>
# {% comment %} {% endblock %} {% endcomment %}


