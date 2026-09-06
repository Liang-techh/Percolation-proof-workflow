# Exact terminal-neighborhood gate for the second candidate

Freeze the second LP coefficient snapshot and the exact M0, M0 inverse, D,
L and mass Fourier rows. Use one predetermined state
q=0, v=(e4+e5)/20, c=w=eta=0 and one predetermined terminal offset
tau=1/100 (t=99/100). No search, trajectory or solver.

The source rows give C=(21/10000000)e1, M=M0 and hence a strictly positive
residual cost E=delta'Ldelta. The candidate has only a8 and c4, with a1=0;
at this state c=0 and all q terms vanish, so its storage derivative is
f'W0+f W0dot with f=a8*tau^8. Check the exact inequality E+Vdot>0.
This rejects the candidate's uniform b=0 gate on a terminal-neighborhood
source state, not the physical reachability theorem or all storage families.
