open Core
open Ast_types

type value =
  | Val_triv
  | Val_bool of bool
  | Val_real of float
  | Val_nat of int
  | Val_abs of string * exp * closure
  | Val_prim of (value -> value Or_error.t)
  | Val_dist of value dist
  | Val_tensor of Tensor.t
  | Val_tuple of value list

and closure = value String.Map.t

type fancy_value =
  | Fval_base of value
  | Fval_poly of (int list -> value option)
