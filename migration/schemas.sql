CREATE TABLE department(
    id SERIAL NOT NULL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL 
);

CREATE TABLE employee(
    emp_id SERIAL PRIMARY KEY,
    user_name VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    passwd TEXT,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    dept INT NOT NULL,
    CONSTRAINT employee_dept_fkey FOREIGN KEY (dept)
        REFERENCES department(id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE hod(
    hod_id INT NOT NULL,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    dept INT NOT NULL,
    PRIMARY KEY(hod_id, start_date),
    CONSTRAINT hod_dept_fkey FOREIGN KEY (dept)
        REFERENCES department(id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT hod_hod_id_fkey FOREIGN kEY (hod_id)
        REFERENCES employee(emp_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE cc_faculty(
    cc_id INT NOT NULL,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    dept INT NOT NULL,
    PRIMARY KEY(cc_id, start_date),
    CONSTRAINT cc_faculty_dept_fkey FOREIGN KEY (dept)
        REFERENCES department(id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION,
    CONSTRAINT cc_faculty_cc_id_fkey FOREIGN kEY (cc_id)
        REFERENCES employee(emp_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE director(
    dir_id INT NOT NULL,
    start_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    end_date TIMESTAMP WITHOUT TIME ZONE,
    PRIMARY KEY(dir_id, start_date),
    CONSTRAINT director_dir_id_fkey FOREIGN kEY (dir_id)
        REFERENCES employee(emp_id) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION
);