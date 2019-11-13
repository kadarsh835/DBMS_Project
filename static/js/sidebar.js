// BS tabs hover (instead - hover write - click)
$('.tab-menu a').hover(function (e) {
    e.preventDefault()
    $(this).tab('show')
})