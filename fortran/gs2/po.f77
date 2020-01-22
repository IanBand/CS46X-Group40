     SUBROUTINE PO (CONC,PHI,NN,IT,STIME,NDIM,RDATE,RTIME)
C
C    PURPOSE: TO GENERATE RESTART DATA FILES
C	          PRESSURES ARE WRITTEN TO TAPE7
C	          CONCENTRATIONS ARE WRITTEN TO TAPE8
C**
     LEVEL 2, CONC,PHI
     DIMENSION CONC(NDIM),PHI(NDIM)
     CHARACTER RDATE*10
     CHARACTER RTIME*10
C
     WRITE (8,1051) RDATE,RTIME
     WRITE (8,1053) IT
     WRITE (8,1054) STIME
     WRITE (8,1056) (I,CONC(I),I=1,NN)
     WRITE (7,1051) RDATE,RTIME
     WRITE (7,1052) IT
     WRITE (7,1055) STIME
     WRITE (7,1056) (I,PHI(I),I=1,NN)
1051 FORMAT ('1 RUN IDENTIFICATION: ',A10,1X,A10)
1052 FORMAT (' PRESSURE HEAD OUTPUT AT TIME STEP:',I4)
1053 FORMAT (' CONCENTRATION OUTPUT AT TIME STEP:',I4)
1054 FORMAT (' TIME (HOURS):	',G15.5)
1055 FORMAT (' TIME (HOURS):	',G15.5)
1056 FORMAT (4(I5,G15.8))
     RETURN
     END