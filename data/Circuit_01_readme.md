# Circuit 01 data

## Columns

1. `Shot_num`: Shot index
2. `Z_gate_cond_bit`: Bit to determine if the `Z` gate was applied
3. `Z_bit_basis`: Bit used in determination of basis (ZX)
4. `X_bit_basis`: Bit used in determination of basis (ZX)
5. `Sdg_gate_applied`: Intersection of `Z_bit_basis` and `X_bit_basis` and tells if the `Sdg` gate was applied or not
6. `H_gate_applied`: Is `X_bit_basis` and tells if the `H` gate was applied  or not
7. `Measure_basis`: Determined by `X_bit_basis` and `Z_bit_basis` (0,0 -> Z, 0,1 -> Z, 1,0 -> X, 1,1 -> Y)
8. `Outcome`: Outcome per shot

