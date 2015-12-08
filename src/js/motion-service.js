var fs = require('fs');
var jf = require('jsonfile');

/**
 * Module implementation of the API for retrieving
 * devicemotion signal data.
 **/
module.exports = {

    /**
     * Motion API for storing devicemotion acceleration values
     *
     * {string} dataDirectory - path where to store the data files
     * {string} id - the id of the datafile
     * {object} data - the acceleration data
     **/
    updateData: function(dataDirectory, id, data) {
       // check that the image exists
       if(typeof id !== "string") {
         console.error("id argument is invalid");
         return;
       }
       var file = dataDirectory+"/"+id+".json"

       jf.writeFileSync(file,JSON.parse(data));
       console.log("updated "+file);
    }
}
