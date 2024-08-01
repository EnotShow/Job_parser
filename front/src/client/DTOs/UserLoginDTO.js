const BaseDTO = require("src/client/BaseDTO");

class UserLoginDTO extends BaseDTO {
    constructor(email, password) {
        super();
        this.email = email;
        this.password = password;
    }
}

export default UserLoginDTO;
