with import <nixpkgs> {} ;

mkShell {
  buildInputs = [
    rshell
    (python3.withPackages (p: with p;[
      pyserial
      black
    ]))
  ];
}
