; Auto-generated. Do not edit!


(cl:in-package yw_tool_base-msg)


;//! \htmlinclude db.msg.html

(cl:defclass <db> (roslisp-msg-protocol:ros-message)
  ((name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (age
    :reader age
    :initarg :age
    :type cl:fixnum
    :initform 0)
   (sex
    :reader sex
    :initarg :sex
    :type cl:fixnum
    :initform 0)
   (x
    :reader x
    :initarg :x
    :type cl:fixnum
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:fixnum
    :initform 0)
   (z
    :reader z
    :initarg :z
    :type cl:fixnum
    :initform 0))
)

(cl:defclass db (<db>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <db>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'db)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name yw_tool_base-msg:<db> is deprecated: use yw_tool_base-msg:db instead.")))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:name-val is deprecated.  Use yw_tool_base-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'age-val :lambda-list '(m))
(cl:defmethod age-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:age-val is deprecated.  Use yw_tool_base-msg:age instead.")
  (age m))

(cl:ensure-generic-function 'sex-val :lambda-list '(m))
(cl:defmethod sex-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:sex-val is deprecated.  Use yw_tool_base-msg:sex instead.")
  (sex m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:x-val is deprecated.  Use yw_tool_base-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:y-val is deprecated.  Use yw_tool_base-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'z-val :lambda-list '(m))
(cl:defmethod z-val ((m <db>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader yw_tool_base-msg:z-val is deprecated.  Use yw_tool_base-msg:z instead.")
  (z m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<db>)))
    "Constants for message type '<db>"
  '((:UNKNOWN . 0)
    (:MALE . 1)
    (:FEMALE . 2))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'db)))
    "Constants for message type 'db"
  '((:UNKNOWN . 0)
    (:MALE . 1)
    (:FEMALE . 2))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <db>) ostream)
  "Serializes a message object of type '<db>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'age)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'sex)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'z)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <db>) istream)
  "Deserializes a message object of type '<db>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'age)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'sex)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'x)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'y)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'z)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<db>)))
  "Returns string type for a message object of type '<db>"
  "yw_tool_base/db")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'db)))
  "Returns string type for a message object of type 'db"
  "yw_tool_base/db")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<db>)))
  "Returns md5sum for a message object of type '<db>"
  "7d5de553dacb8637be45c28569c7098a")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'db)))
  "Returns md5sum for a message object of type 'db"
  "7d5de553dacb8637be45c28569c7098a")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<db>)))
  "Returns full string definition for message of type '<db>"
  (cl:format cl:nil "string name~%uint8  age~%uint8  sex~%uint8  x~%uint8  y~%uint8  z~%~%uint8 unknown = 0~%uint8 male    = 1~%uint8 female  = 2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'db)))
  "Returns full string definition for message of type 'db"
  (cl:format cl:nil "string name~%uint8  age~%uint8  sex~%uint8  x~%uint8  y~%uint8  z~%~%uint8 unknown = 0~%uint8 male    = 1~%uint8 female  = 2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <db>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'name))
     1
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <db>))
  "Converts a ROS message object to a list"
  (cl:list 'db
    (cl:cons ':name (name msg))
    (cl:cons ':age (age msg))
    (cl:cons ':sex (sex msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':z (z msg))
))
