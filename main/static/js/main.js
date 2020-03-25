$("*[data-increment]").click(function() {
  var target = $(this.dataset.increment);
  target.val(function(i, orig) {
    return parseInt(orig) + 1;
  });
  target.trigger("change");
  return false;
});

$("*[data-decrement]").click(function() {
  var target = $(this.dataset.decrement);
  target.val(function(i, orig) {
    return Math.max(0, parseInt(orig) - 1);
  });
  target.trigger("change");
  return false;
});

$("*[data-limit]")
  .change(function() {
    if (parseInt(this.dataset.limit) >= parseInt(this.value)) {
      $(this).removeClass("bg-warning");
    } else {
      $(this).addClass("bg-warning");
    }
  })
  .trigger("change");
