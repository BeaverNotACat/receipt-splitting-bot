{
  pkgs ? import <nixpkgs> { },
}:

pkgs.mkShell {
  nativeBuildInputs = [
    pkgs.zlib
    pkgs.stdenv
    pkgs.graphviz
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${
      pkgs.lib.makeLibraryPath [
        pkgs.zlib
        pkgs.stdenv.cc.cc.lib
      ]
    };
    fish
  '';
}
