{
  description = "A python Dev flake!";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
  };

  outputs = { nixpkgs, ... }@inputs:
 let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
  in
 {
    devShells.${system} = {
    default = pkgs.mkShell {
     nativeBuildInputs = with pkgs; [
      python3
    ];

    shellHook = "echo Welcome to python environment";
   };
  };
 };
}
