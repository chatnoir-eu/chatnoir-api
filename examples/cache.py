from chatnoir_api import cache_contents, ShortUUID

contents = cache_contents(
    "clueweb09-en0051-90-00849",
    index="clueweb09",
)
print(contents)

plain_contents = cache_contents(
    "clueweb09-en0051-90-00849",
    index="clueweb09",
    plain=True,
)
print(plain_contents)

contents = cache_contents(
    ShortUUID("MzOlTIayX9ub7c13GLPr_g"),
    index="clueweb22/b",
)
print(contents)

plain_contents = cache_contents(
    ShortUUID("MzOlTIayX9ub7c13GLPr_g"),
    index="clueweb22/b",
    plain=True,
)
print(plain_contents)
