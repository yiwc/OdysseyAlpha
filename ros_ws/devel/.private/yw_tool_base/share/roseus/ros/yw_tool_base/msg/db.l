;; Auto-generated. Do not edit!


(when (boundp 'yw_tool_base::db)
  (if (not (find-package "YW_TOOL_BASE"))
    (make-package "YW_TOOL_BASE"))
  (shadow 'db (find-package "YW_TOOL_BASE")))
(unless (find-package "YW_TOOL_BASE::DB")
  (make-package "YW_TOOL_BASE::DB"))

(in-package "ROS")
;;//! \htmlinclude db.msg.html


(intern "*UNKNOWN*" (find-package "YW_TOOL_BASE::DB"))
(shadow '*UNKNOWN* (find-package "YW_TOOL_BASE::DB"))
(defconstant yw_tool_base::db::*UNKNOWN* 0)
(intern "*MALE*" (find-package "YW_TOOL_BASE::DB"))
(shadow '*MALE* (find-package "YW_TOOL_BASE::DB"))
(defconstant yw_tool_base::db::*MALE* 1)
(intern "*FEMALE*" (find-package "YW_TOOL_BASE::DB"))
(shadow '*FEMALE* (find-package "YW_TOOL_BASE::DB"))
(defconstant yw_tool_base::db::*FEMALE* 2)
(defclass yw_tool_base::db
  :super ros::object
  :slots (_name _age _sex _x _y _z ))

(defmethod yw_tool_base::db
  (:init
   (&key
    ((:name __name) "")
    ((:age __age) 0)
    ((:sex __sex) 0)
    ((:x __x) 0)
    ((:y __y) 0)
    ((:z __z) 0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _age (round __age))
   (setq _sex (round __sex))
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _z (round __z))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:age
   (&optional __age)
   (if __age (setq _age __age)) _age)
  (:sex
   (&optional __sex)
   (if __sex (setq _sex __sex)) _sex)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:z
   (&optional __z)
   (if __z (setq _z __z)) _z)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; uint8 _age
    1
    ;; uint8 _sex
    1
    ;; uint8 _x
    1
    ;; uint8 _y
    1
    ;; uint8 _z
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; uint8 _age
       (write-byte _age s)
     ;; uint8 _sex
       (write-byte _sex s)
     ;; uint8 _x
       (write-byte _x s)
     ;; uint8 _y
       (write-byte _y s)
     ;; uint8 _z
       (write-byte _z s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _age
     (setq _age (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _sex
     (setq _sex (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _x
     (setq _x (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _y
     (setq _y (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _z
     (setq _z (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get yw_tool_base::db :md5sum-) "7d5de553dacb8637be45c28569c7098a")
(setf (get yw_tool_base::db :datatype-) "yw_tool_base/db")
(setf (get yw_tool_base::db :definition-)
      "string name
uint8  age
uint8  sex
uint8  x
uint8  y
uint8  z

uint8 unknown = 0
uint8 male    = 1
uint8 female  = 2

")



(provide :yw_tool_base/db "7d5de553dacb8637be45c28569c7098a")


