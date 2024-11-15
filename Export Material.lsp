(defun c:exportmaterial () 
  (defun getblockattributes (blk / enx) 
    (if 
      (and (setq blk (entnext blk)) 
           (= "ATTRIB" (cdr (assoc 0 (setq enx (entget blk)))))
           (or 
             (= "NAME" (cdr (assoc 2 enx)))
             (= "MATERIAL" (cdr (assoc 2 enx)))
           ) ;or
      ) ;and
      (cons 
        (cons 
          (cdr (assoc 2 enx))
          (cdr (assoc 1 (reverse enx)))
        ) ;cons
        (getblockattributes blk)
      ) ;cons
    ) ;if
  ) ;defun
(initdia)
  (setq panelname        (getstring T "\nPanel name (e.g. Panel A1): ")
        paneldescription (getstring T "\nPanel description: ")
        ss               (ssget (list (cons 0 "INSERT")))
        c                0
        file             (open "C:\\Users\\lwooten\\Desktop\\Relaying Material Python\\materialList\\Exported Material from AutoCAD.csv" 
                               "a"
                         )
  )

  (repeat (sslength ss) 
    (setq lst (getblockattributes (ssname ss c)))
    (foreach n lst
      (setq itemnumber (cdr (assoc "MATERIAL" lst))
            devicename (cdr (assoc "NAME" lst))
      );setq
      (write-line 
        (strcat  itemnumber
                ","
                (if (not devicename) "\"\"" devicename)
                ","
                panelname
                "|"
                paneldescription
        )
        file
      )
    )
    (setq c (1+ c))
  )
  (close file)
)
(c:exportmaterial)