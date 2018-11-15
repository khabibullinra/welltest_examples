------------------------------------ Schedule Section -----------------------------
SCHEDULE
WELSPECS
-- name group x y pwf_depth phase /
  M1     G1   19 75 1*        OIL /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   M1   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WELSPECS
-- name group x y pwf_depth phase /
  M2     G1   29 85 1*        OIL /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   M2   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   PS1    SHUT  BHP           3*          10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   M1    OPEN  LRAT           3*          100        1*   1* /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   M2    OPEN  LRAT           3*          100        1*   1* /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   PS2    SHUT  BHP           3*          10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   PS1    OPEN  BHP           3*          1*        1*   100 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I2   WATER  SHUT  BHP     10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   PS2    OPEN  BHP           3*          1*        1*   100 /
/
TSTEP
 1*1.0
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I2   WATER  OPEN  BHP     1*        1*   400 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P3    SHUT  BHP           3*          10        1*   50 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I1   WATER  SHUT  BHP     10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P3    OPEN  BHP           3*          1*        1*   100 /
/
TSTEP
 1*1.0
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I1   WATER  OPEN  BHP     1*        1*   400 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P5    SHUT  BHP           3*          10        1*   50 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I5   WATER  SHUT  BHP     10        1*   50 /
/
TSTEP
 1*1.0
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P5    OPEN  BHP           3*          1*        1*   100 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P4    SHUT  BHP           3*          10        1*   50 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I5   WATER  OPEN  BHP     1*        1*   400 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I6   WATER  SHUT  BHP     10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P4    OPEN  BHP           3*          1*        1*   100 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P6    SHUT  BHP           3*          10        1*   50 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I6   WATER  OPEN  BHP     1*        1*   400 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I4   WATER  SHUT  BHP     10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P6    OPEN  BHP           3*          1*        1*   100 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P1    SHUT  BHP           3*          10        1*   50 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I4   WATER  OPEN  BHP     1*        1*   400 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I3   WATER  SHUT  BHP     10        1*   50 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   P1    OPEN  BHP           3*          1*        1*   100 /
/
TSTEP
 3*0.67
/
WELSPECS
-- name group x y pwf_depth phase /
  MI1     G1   24 8 1*        WATER /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   MI1   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WELSPECS
-- name group x y pwf_depth phase /
  Ì6     G1   19 51 1*        OIL /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   Ì6   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   MI1   WATER  OPEN  BHP     1*        1*   350 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   Ì6    OPEN  LRAT           3*          100        1*   1* /
/
WCONINJE
-- name fluid status control lrate lrateres bhp /
   I3   WATER  OPEN  BHP     1*        1*   400 /
/
TSTEP
 3*10.33
/
WELSPECS
-- name group x y pwf_depth phase /
  Ì5     G1   51 19 1*        OIL /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   Ì5   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WELSPECS
-- name group x y pwf_depth phase /
  Ì4     G1   85 51 1*        OIL /
/
COMPDAT
-- name x y z1 z2 perf table  CF  diam KH skin  /
   Ì4   2*   1 13  OPEN     2*      0.2  1*  1 /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   Ì5    OPEN  LRAT           3*          200        1*   1* /
/
WCONPROD
-- name status control orate wrate grate lrate lrateres bhp /
   Ì4    OPEN  LRAT           3*          50        1*   1* /
/
TSTEP
 3*10.33
/
