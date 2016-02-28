//code recommended at https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i=0; i<cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length+1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    //these HTTP methods do not require CSRF protection
    return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    //Allow absolute or scheme relative URLs to the same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative
    !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            //send the token to same-origin, relative URLs only.
            //send the token only if the method warrants CSRF protection
            //using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){

  // Show fn options for user
  $('input.show-options').on('click', function(){
    var $this = $(this);
    var el_id = $this.attr('id');
    var fn_type = el_id.split('_')[1];
    var ul_identifier = 'ul.' + fn_type + '-options';
    $(ul_identifier).toggleClass('hidden');
  })

  // Plot action
  $('#submit').on('click', function(){

    if (!is_valid())
      return false;

    $.ajax({
      url: window.GET_IMAGE_URL,
      type: 'POST',
      contentType : 'application/json',
      data: get_data()
    })
    .done(function(_data){
      $("#plot").attr('src', 'data:image/jpeg;base64,' + _data);
    })
    .fail(function() {
      alert( "Ops, deu ruim no servidor. Por favor nao tire nosso 10." );
    });


  });

  function is_valid() {
    // If no function is selected
    if ($('.fn-options:not(.hidden)').length == 0) {
      alert('At least one function should be ploted');
      return false;
    }
    result = true;
    // If required is empty
    $('.required').each(function(){
      var $el = $(this);
      if (!$el.val()) {
        alert($el.attr('id') + ' is required');
        result = false;
        return false;
      }
    });
    return result;
  }

  function get_value(selector, default_value, type) {
    var value = $(selector).val();
    if (!value)
      value = default_value;
    if (type == undefined || type == 'int')
      return parseFloat(value, 10);
    return value;
  }

  function get_fn_options(fn_type) {
    var $ul = $('.' + fn_type + '-options');
    // It's not supposed to show
    if ($ul.hasClass('hidden'))
      return null;

    var options = {
      'type': fn_type
    };

    $('input', $ul).each(function() {
      var $el = $(this);
      var data_type = $el.data('data_type');
      var key = $el.attr('id').split('-')[1];
      var value = $el.val();
      if (fn_type == 'poly' && key == 'coef') {
        value = value.split(',');
        $.each(value, function(index, val){
          value[index] = parseFloat(val, 10);
        });
      } else {
        if (data_type == 'int')
          value = parseFloat(value, 10);
      }
      options[key] = value;
    })

    return options;

  }

  function get_data() {
    var fn_data = [];
    var cos_fn = get_fn_options('cos');
    var sin_fn = get_fn_options('sin');
    var poly_fn = get_fn_options('poly');
    if (cos_fn) fn_data.push(cos_fn);
    if (sin_fn) fn_data.push(sin_fn);
    if (poly_fn) fn_data.push(poly_fn);

    var data = {
          'plot': {
              'xrange': [
                get_value('#xrange-0'),
                get_value('#xrange-1'),
                get_value('#xrange-2'),
                ],
              'xlimits': [
                get_value('#xlimits-0', null),
                get_value('#xlimits-1', null),
                ],
              'ylimits': [
                get_value('#ylimits-0', null),
                get_value('#ylimits-1', null),
                ],
              'xlabel': get_value('#xlabel', '', 'str'),
              'ylabel': get_value('#ylabel', '', 'str'),
              'title': get_value('#title', '', 'str'),
              'show_grid': $('#show_grid').is(":checked"),
          },
          'fn': fn_data        
      };
    return JSON.stringify(data);
  }

});