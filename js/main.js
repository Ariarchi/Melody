$(document).ready(function () {
  var currentFloor = 2;
  var counterUp = $(".counter-up");
  var counterDown= $(".counter-down");
  var floorPath = $(".home__image path");
  var modal = $(".modal");
  var modalCloseButton = $(".modal__close-button");
  var viewFlatsButton = $(".view-flats");
  var modalPath = $(".flats path");

  //Функция при навелении мышки на этаж
  floorPath.on("mouseover", function () {
    floorPath.removeClass("current-floor");
    currentFloor = $(this).attr("data-floor");
    $(".counter").text(currentFloor);
  });

  floorPath.on("click", toggleModal); /*При клике на этаж, вызывается окно*/
  modalCloseButton.on("click", toggleModal); /*При клике на кнопку, закрывает окно */
  viewFlatsButton.on("click", toggleModal);

  //Функция при клике мышки на стрелку вверх
  counterUp.on("click", function () {
    if (currentFloor < 18) {
      currentFloor++;
      usCurrentFloor = currentFloor.toLocaleString('en-US', { minimumIntegerDigits: 2, useGroupping: false}); //форматирование числа с 1 на 01
      $(".counter").text(usCurrentFloor);
      floorPath.removeClass("current-floor");
      $(`[data-floor=${usCurrentFloor}]`).toggleClass("current-floor");
    }
  });

    //Функция при клике мышки на стрелку вниз
    counterDown.on("click", function () {
    if (currentFloor >2) {
      currentFloor--;
      usCurrentFloor = currentFloor.toLocaleString('en-US', { minimumIntegerDigits: 2, useGroupping: false}); //форматирование числа с 1 на 01
      $(".counter").text(usCurrentFloor);
      floorPath.removeClass("current-floor");
      $(`[data-floor=${usCurrentFloor}]`).toggleClass("current-floor"); //подсветка текущего этажа
    }
  });

  function toggleModal() { //функция открыть/закрыть окно
    modal.toggleClass("is__open");
  }

  modalPath.on("mouseover", function () {
    modalPath.removeClass("current-flats");
    currentFloor = $(this).attr("data-floor");
    $(".counter").text(currentFloor);
  });
  
});