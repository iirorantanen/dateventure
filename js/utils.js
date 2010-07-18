<!-- $Id$ -->
function validateFormFields($containerToValidate)
{
    //TODO: move this to a utils.js
    var $elementsToValidate = $(':input', $containerToValidate);
    var returnValue = true;
    //define default validation patterns and standard messages.
    var integer_pattern = /^[\-|\+]?\d+$/;
    var integer_message = 'Please enter a valid number';
    var float_pattern = /^[\-|\+]?(?:\d*\.?\d+|\d+\.)$/;
    var float_message = 'Please enter a valid number';
    var email_pattern = /^[a-zA-Z0-9]([\w\-\.\+]*)@([\w\-\.]*)(\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2}){0,2})$/i;
    var email_message = 'Please enter a valid email';
    var multipleEmail_pattern = /^(?:[a-zA-Z0-9]([\w\-\.\+]*)@([\w\-\.]*)(\.[a-zA-Z]{2,4}(\.[a-zA-Z]{2}){0,2}),?\s*)+$/i;
    var multipleEmail_message = 'Please enter a valid email ids';
    var id_pattern = /^([\w-]+(?:[\w-]+)*)$/i;
    var id_message = 'Please enter a valid id. Special characters are not allowed';
    //var url_pattern = /^(?:(?:\w|\d)+\.)+[a-zA-Z0-9]{2,6}$/;
    var url_pattern = /^[http:\/\/][https:\/\/]/;
    var url_message = 'Please enter a valid URL';
    var age_pattern = /^1[89]|[2-9]\d|[1-9]\d{2,}/;
    var age_message = 'Palvelu on sallittu vain 18 vuotta täyttäneille';
    var hour_pattern = /^0[0-9]|1[0-9]|2[0-3]/;
    var hour_message = 'Anna kellonaika muodossa HH:MM';
//    var min_pattern = /^[0-59]/;
//    var min_message = 'Anna kellonaika muodossa HH:MM';
    var pattern_message = 'Sorry. The entered value does not match the required pattern';
    //start the validation process.
    $elementsToValidate
    .filter('[trim="true"]').each(function(index, eachItem)
    {    //remove all spaces from fields that are marked as trim
        $(eachItem).val($.trim($(eachItem).val()));
    })//.filter('[trim="true"]').each(function(index, eachItem)
    .end() //remove the previous filter
    .filter('[mandatory="true"]').each(function(index, eachItem)
    {
        var $eachItem = $(eachItem);
        //Check if the mandatory fields have a value
        if($eachItem.val() == "" || $eachItem.val() == "-1" )
        {
            message = getCustomMessage ($eachItem, $eachItem.attr('title') + " Täytäthän kaikki kentät");
            showError ($eachItem,message);
            returnValue = false;
        }//if($eachItem.val() == "")
    })//$elementsToValidate.filter('[mandatory="true"]').each()
    .end() //remove the previous filter
    .filter('[dataType]').each(function(index, eachItem)
    {
        var $eachItem = $(eachItem);
        var valueToValidate = $eachItem.val();
        if(valueToValidate && valueToValidate != '')
        {
            var dataType = $eachItem.attr('dataType');
            try
            {
            var patternToCheck = eval(dataType + '_pattern');
            var defaultMessage = eval (dataType + '_message');
            if (valueToValidate.match(patternToCheck) == null)
            {
                showError ($eachItem, getCustomMessage($eachItem, defaultMessage));
                returnValue = false;
            }//if ($eachItem.val().match(patternToCheck) == null)
            }catch(e){return;}
        }//if(valueToValidate != '')
    })//.filter('[dataType]').each(function(index, eachItem)
    .end() //remove the previous filter
    .filter('[pattern]').each(function(index, eachItem)
    {
        //validate for a specified pattern
        var $eachItem = $(eachItem);
        var valueToValidate = $eachItem.val();
        if(valueToValidate && valueToValidate != '')
        {
            var patternToCheck = eval($eachItem.attr('pattern'));
            var defaultMessage = eval ('pattern_message');
            if (valueToValidate.match(patternToCheck) == null)
            {
                showError ($eachItem, getCustomMessage($eachItem, defaultMessage));
                returnValue = false;
            }
        }//if(valueToValidate != '')
    });//.filter('[pattern]').each(function(index, eachItem)
    return returnValue;
}//function validate($containerToValidate)

function showError($field,message)
{

    var errorLocation = $field.attr("name")+"_Error";
    $('#'+errorLocation).html("<font color='red'>" + message + "</font>").show()
    //setTimeout("$('#"+errorLocation+"').addClass('error')",2000);
    setTimeout("$('#"+errorLocation+"').html('')",5000);

}//function showError()

function getCustomMessage ($field, defaultMessage)
{
    customMessage = $field.attr('message');
    if (!customMessage || customMessage == "") {customMessage = defaultMessage;}
    return customMessage;
}
/**
 * Retruns the x position of the given object in the window / screen.
 */
function findPosX(obj) {
	var curleft = 0;
	if (document.getElementById || document.all) {
		curleft += document.body.offsetLeft;
		while (obj.offsetParent) {
			curleft += obj.offsetLeft;
			obj = obj.offsetParent;
		}
	}
	else if (document.layers) {
		curleft += obj.x;
	}
	return curleft;
}

/**
 * Retruns the x position of the given object in the window / screen.
 */
function findPosY(obj) {
	var curtop = 0;
	if (document.getElementById || document.all) {
		curtop += document.body.offsetTop;
		while (obj.offsetParent) {
			curtop += obj.offsetTop;
			obj = obj.offsetParent;
		}
	} else if (document.layers) {
		curtop += obj.y;
	}
	return curtop;
}
