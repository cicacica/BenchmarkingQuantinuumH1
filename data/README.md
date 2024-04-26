# Information on data

# Circuit 01 data

## Columns

1. `Shot_num`: Represents the index of the shot.
2. `z_gate_cond_bit`: Bit indicating whether the `Z` gate was applied.
3. `z_bit_basis`: Bit used in the determination of the basis (ZX).
4. `x_bit_basis`: Bit used in the determination of the basis (ZX).
5. `Sdg_gate_applied`: Intersection of `z_bit_basis` and `x_bit_basis`, indicating whether the `Sdg` gate was applied.
6. `H_gate_applied`: Intersection with `x_bit_basis`, indicating whether the `H` gate was applied.
7. `Measure_basis`: Determined by `x_bit_basis` and `z_bit_basis` (0,0 -> Z, 0,1 -> Z, 1,0 -> X, 1,1 -> Y).
8. `Outcome`: Represents the outcome of the measurement.

# Circuit 02 data

## Columns

1. `Shot_num`: Represents the shot number.
2. `pi_res_bits`: Contains the results for bits after applying a pi rotation.
3. `half_pi_res_bits`: Contains the results for bits after applying a rotation of half pi.
4. `quarter_pi_res_bits`: Contains the results for bits after applying a rotation of quarter pi.
5. `z_bit_basis`: Represents the basis used for measurement (Z basis).
6. `x_bit_basis`: Represents the basis used for measurement (X basis).
7. `Sdg_gate_applied`: Indicates whether the Sdg gate was applied.
8. `H_gate_applied`: Indicates whether the H gate was applied.
9. `Rotation_int`: Represents the rotation angle in integers taken from `pi_res_bits`, `half_pi_res_bits` and `quarter_pi_res_bits` (eg - 0,0,0 -> 0, or 0,1,0 -> 2 in little endian format. Using three conditional bit registers to generate 0..7 for the j in j*pi/4)
10. `Measure_basis`: Determined by `x_bit_basis` and `z_bit_basis` (0,0 -> Z, 0,1 -> Z, 1,0 -> X, 1,1 -> Y).
11. `Outcome`: Represents the outcome of the measurement.
