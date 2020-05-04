load harness


@test "Hatim-Madkhaki-1" {
  check 'if ¬ true then x := 7 else Y := 7' '⇒ Y := 7, {}
⇒ skip, {Y → 7}'
}

@test "Hatim-Madkhaki-2" {
  check 'while h * h < L - y do skip' '⇒ skip, {}'
}


@test "Hatim-Madkhaki-3" {
  check 'if true then x := 2 else x := 0' '⇒ x := 2, {}
⇒ skip, {x → 2}'
}

@test "Hatim-Madkhaki-4" {
  check 'if false then while true do skip else x := 7' '⇒ x := 7, {}
⇒ skip, {x → 7}'
}

@test "Hatim-Madkhaki-5" {
  check 'while false do x := 7 ; y := 7' '⇒ skip; y := 7, {}
⇒ y := 7, {}
⇒ skip, {y → 7}'
}

@test "Hatim-Madkhaki-6" {
  check 'x := 7' '⇒ skip, {x → 7}'
}

@test "Hatim-Madkhaki-7" {
  check 'x := 5' '⇒ skip, {x → 5}'
}
