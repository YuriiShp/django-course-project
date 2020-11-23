//
// // Prevent closing from click inside dropdown
// $(document).on('click', '.dropdown-menu', function (e) {
//   e.stopPropagation();
// });
//
// // make it as accordion for smaller screens
// if ($(window).width() < 992) {
//   $('.dropdown-menu a').click(function(e){
//     e.preventDefault();
//       if($(this).next('.submenu').length){
//         $(this).next('.submenu').toggle();
//       }
//       $('.dropdown').on('hide.bs.dropdown', function () {
//      $(this).find('.submenu').hide();
//   })
//   });
// }
//
//
// $('#znyzhka').click(function(e){
//   if (e.target.checked) {
//     localStorage.checked = true;
//   } else {
//     localStorage.checked = false;
//   }
// })
//
// $( document ).ready(function() {
//
//   flag = localStorage.checked
//   document.querySelector('#znyzhka').checked = flag
//
//
// });
document.querySelectorAll('#sale input#check')[1].onclick = function(){
  console.log("ok")
}
