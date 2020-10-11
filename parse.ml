open Core

exception Parser_error of string * Location.t

let token lexbuf =
  Result.try_with (fun () -> Lexer.token lexbuf)

let wrap parsing_fun lexbuf =
  let ast = parsing_fun lexbuf in
  Parsing.clear_parser ();
  ast

let rec loop lexbuf checkpoint =
  let module I = Parser.MenhirInterpreter in
  match checkpoint with
  | I.InputNeeded _ ->
    Result.Let_syntax.(
      let%bind token = token lexbuf in
      let triple = (token, lexbuf.Lexing.lex_start_p, lexbuf.Lexing.lex_curr_p) in
      let checkpoint = I.offer checkpoint triple in
      loop lexbuf checkpoint
    )
  | I.Shifting _
  | I.AboutToReduce _ ->
    loop lexbuf (I.resume checkpoint)
  | I.Accepted v -> Ok v
  | I.Rejected ->
    let loc = Location.curr lexbuf in
    Error (Parser_error ("Syntax error", loc))
  | I.HandlingError env ->
    let loc = Location.curr lexbuf in
    let state =
      match I.stack env with
      | lazy Nil -> 0
      | lazy (Cons (I.Element (state, _, _, _), _)) -> I.number state
    in
    let msg = (* try Parser_messages.message state with _ -> *) "Syntax error: state " ^ Int.to_string state in
    Error (Parser_error (msg, loc))

let wrap_menhir entry lexbuf =
  let initial = entry lexbuf.Lexing.lex_curr_p in
  wrap (fun lexbuf -> loop lexbuf initial) lexbuf

let implementation = wrap_menhir Parser.Incremental.implementation

let () =
  Location.register_error_of_exn
    (function
      | Parser_error (msg, loc) -> Some (Location.errorf ~loc "%s" msg)
      | _ -> None
    )
