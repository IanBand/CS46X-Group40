      SUBROUTINE GELB (R,A,M,N,MUD,MLD,EPS,IER,MAXR,MAXA)
C
C     PURPOSE: TO SOLVE THE MASS-TRANSPORT EQUATION
C**
      LEVEL 2, A
      DIMENSION A(MAXA),R(MAXR)
C
C	TEST ON WRONG INPUT PARAMETERS
      IF(MLD) 47,1,1
    1 IF(MUD) 47,2,2
    2 MC=1+MLD+MUD
      IF(MC+1-M-M)3,3,47
C
C	PREPARE INTEGER PARAMETERS
C	    MC=NUMBER OF COLUMNS IN MATRIX A
C	    MU-NUMBER OF ZEROS TO BE INSERTED IN FIRST ROW OF MATRIX A
C	    ML=NUMBER OF MISSING ELEMENTS IN LAST ROW OF MATRIX A
C	    MR=INDEX OF LAST ROW IN MATRIX A WITH MC ELEMENTS
C	    MZ=TOTAL NUMBER OF ZEROS TO BE INSERTED IN MATRIX A
C	    MA=TOTAL NUMBER OF STORAGE LOCATIONS NECESSARY FOR MATRIX A
C	    NM=NUMBER OF ELEMENTS IN MATRIX R
    3 IF(MC-M)5,5,4
    4 MC=M
    5 MU=MC-MUD-1
      ML=MC-MLD-1
      MR=M-ML
      MZ=(MU*(MU+1))/2
      MA=M*MC-(ML*(ML+1))/2
      NM=N*M
C
C     MOVE ELEMENTS BACKWARD AND SEARCH FOR ABSOLUTELY GREATEST ELEMENT
      IER=0
      PIV=0.
      IF(MLD)14,14,6
    6 JJ=MA
      J=MA-MZ
      KST=J
      DO 9 K=1,KST
      TB=A(J)
      A(JJ)=TB
      TB=ABS(TB)
      IF(TB-PIV)8,8,7
    7 PIV=TB
    8 J=J-1
    9 JJ=JJ-1
C
C     INSERT ZEROS IN FIRST MU ROWS (NOT NECESSARY IN CASE MZ=0)
      IF(MZ)14,14,10
   10 JJ=1
      J=1+MZ
      IC=1+MUD
      DO 13 I=1,MU
      DO 12 K=1,MC
      A(JJ)=0.
      IF(K-IC)11,11,12
   11 A(JJ)=A(J)
      J=J+1
   12 JJ=JJ+1
   13 IC=IC+1
C
C	GENERATE TEST VALUE FOR SINGULARITY
   14 TOL=EPS*PIV
C
C	START DECOMPOSITION LOOP
      KST=1
      IDST=MC
      IC=MC-1
      DO 38 K=1,M
      IF(K-MR-1)16,16,15
   15 IDST=IDST-1
   16 ID=IDST
      ILR=K+MLD
      IF(ILR-M)18,18,17
   17 ILR=M
   18 II=KST
C
C     PIVOT SEARCH IN FIRST COLUMN (ROW INDEXES FROM I=K UP TO I=ILR)
      PIV=0.
      DO 22 I=K,ILR
      TB=ABS(A(II))
      IF(TB-PIV)20,20,19
   19 PIV=TB
      J=I
      JJ=II
   20 IF(I-MR)22,22,21
   21 ID=ID-1
   22 II=II+ID
C
C     TEST ON SINGULARITY
      IF(PIV)47,47,23
   23 IF(IER)26,24,26
   24 IF(PIV-TOL)25,25,26
   25 IER=K-1
   26 PIV=1./A(JJ)
C
C     PIVOT ROW REDUCTION AND ROW INTERCHANGE IN RIGHT HAND SIDE R
      ID=J-K
      DO 27 I=K,NM,M
      II=I+ID
      TB=PIV*R(II)
      R(II)=R(I)
   27 R(I)=TB
C
C     PIVOT ROW REDUCTION AND ROW INTERCHANGE IN COEFFICIENT MATRIX A
      II=KST
      J=JJ+IC
      DO 28 I=JJ,J
      TB=PIV*A(I)
      A(I)=A(II)
      A(II)=TB
   28 II=II+1
C
C     ELEMENT REDUCTION
      IF(K-ILR)29,34,34
   29 ID=KST
      II=K+1
      MU=KST+1
      MZ=KST+IC
      DO 33 I=II,ILR
C
C     IN MATRIX A
      ID=ID+MC
      JJ=I-MR-1
      IF(JJ)31,31,30
   30 ID=ID—JJ
   31 PIV=-A(ID)
      J=ID+1
      DO 32 JJ=MU,MZ
      A(J-1)=A(J)+PIV*A(JJ)
   32 J=J+1
      A(J-1)=0.
C
C     IN MATRIX R
      J=K
      DO 33 JJ=I,NM,M
      R(JJ)=R(JJ)+PIV*R(J)
      J=J+M
   33 CONTINUE
   34 KST=KST+MC
      IF(ILR-MR)36,35,35
   35 IC=IC-1
   36 ID=K-MR
      IF(ID)38,38,37
   37 KST=KST-ID
   38 CONTINUE
C     END OF DECOMPOSITION LOOP
C
C     BACK SUBSTITUTION
      IF(MC-1)46,46,39
   39 IC=2
      KST=MA+ML-MC+2
      II=M
      DO 45 I=2,M
      KST=KST-MC
      II=II-1
      J=II-MR
      IF(J)41,41,40
   40 KST=KST+J
   41 DO 43 J=II,NM,M
      TB=R(J)
      MZ=KST+IC-2
      ID=J
      DO 42 JJ=KST,MZ
      ID=ID+1
   42 TB=TB-A(JJ)*R(ID)
      R(J)=TB
   43 CONTINUE
      IF(IC-MC)44,45,45
   44 IC=IC+1
   45 CONTINUE
   46 RETURN
C
C     ERROR RETURN
   47 IER=—1
      RETURN
      END