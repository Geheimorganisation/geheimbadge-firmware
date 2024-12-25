with import <nixpkgs> {} ;

mkShell {
  buildInputs = [
    rshell
    esptool
    (python3.withPackages (p: with p;[
      pyserial
      black
    ]))
  ];
}
