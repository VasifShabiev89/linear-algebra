"""Translation catalogs (en / ru)."""

from __future__ import annotations

EN: dict = {
    "app.title": "Linear algebra",
    "home.subtitle": "Interactive visualizations. Choose a topic:",
    "home.footer": "New topics will appear here as they are added.",
    "home.open": "Open →",
    "nav.back": "← All topics",
    "nav.btn_prev": "← Back",
    "nav.btn_next": "Next →",
    "section.plane": "Plane",
    "section.preset": "Preset",
    "section.step": "Step",
    "section.explanation": "Explanation",
    "section.matrix": "Matrix",
    "section.vector_v": "Vector v",
    "section.vector_a": "Vector a",
    "section.vector_b": "Vector b",
    "topic.proekcia.title": "Vector projection onto a plane",
    "topic.proekcia.subtitle": "Step-by-step formula walkthrough with an interactive 3D plot.",
    "topic.proekcia.tag": "3D",
    "topic.skalyarnoe.title": "Dot product",
    "topic.skalyarnoe.subtitle": "Definition, angle, orthogonality, and projection onto a direction.",
    "topic.skalyarnoe.tag": "3D",
    "topic.rang.title": "Matrix rank",
    "topic.rang.subtitle": "Columns, span, independence, and the rank theorem.",
    "topic.rang.tag": "3D",
    "proekcia.page_title": "Projection",
    "proekcia.preset.xy.label": "1 — xy plane",
    "proekcia.preset.xy.hint": "Orthogonal basis: residual is strictly along z",
    "proekcia.preset.tilted.label": "2 — tilted plane",
    "proekcia.preset.tilted.hint": "a₁ and a₂ are not orthogonal — use (AᵀA)⁻¹Aᵀv",
    "proekcia.preset.general.label": "3 — general v",
    "proekcia.preset.general.hint": "Typical case: v outside the plane",
    "proekcia.steps": [
        {
            "id": "0",
            "title": "0. Plane W and basis u₁, u₂",
            "explain": "W is a plane. u₁ and u₂ are orthonormal vectors in W (uᵢ·uⱼ = 0, |uᵢ| = 1).",
            "formula": "proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂",
        },
        {
            "id": "1",
            "title": "1. Scalar v·u₁",
            "explain": "v·u₁ is the signed length of the “shadow” of v on axis u₁ — the coefficient along u₁.",
            "formula": "v·u₁ = ?",
        },
        {
            "id": "2",
            "title": "2. Vector (v·u₁)u₁",
            "explain": "Multiply unit u₁ by the scalar — get the component of v along u₁.",
            "formula": "(v·u₁)u₁",
        },
        {
            "id": "3",
            "title": "3. Scalar v·u₂",
            "explain": "Same for the second direction: scalar projection onto u₂.",
            "formula": "v·u₂ = ?",
        },
        {
            "id": "4",
            "title": "4. Vector (v·u₂)u₂",
            "explain": "Second component — the part of v along u₂, lying in plane W.",
            "formula": "(v·u₂)u₂",
        },
        {
            "id": "5",
            "title": "5. Sum = proj_W(v)",
            "explain": "Add both components — projection of v onto the whole plane W.",
            "formula": "(v·u₁)u₁ + (v·u₂)u₂ = proj_W(v)",
        },
        {
            "id": "6",
            "title": "6. Residual v − proj",
            "explain": "The difference v − proj is orthogonal to the plane: residual ⊥ u₁ and ⊥ u₂.",
            "formula": "v = proj_W(v) + (v − proj_W(v))",
        },
    ],
    "proekcia.stats.header": "Formula:  proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂",
    "proekcia.stats.check": "Check: comp₁ + comp₂ = proj ?  {ok}",
    "skalyarnoe.page_title": "Dot product",
    "skalyarnoe.preset.acute.label": "Acute angle",
    "skalyarnoe.preset.acute.hint": "a·b > 0, cos φ > 0",
    "skalyarnoe.preset.right.label": "Right angle",
    "skalyarnoe.preset.right.hint": "a ⊥ b, a·b = 0",
    "skalyarnoe.preset.obtuse.label": "Obtuse angle",
    "skalyarnoe.preset.obtuse.hint": "a·b < 0",
    "skalyarnoe.preset.parallel.label": "Parallel",
    "skalyarnoe.preset.parallel.hint": "b = 2a, cos φ = 1",
    "skalyarnoe.steps": [
        {
            "id": "0",
            "title": "0. Definition",
            "explain": (
                "The dot product of two vectors is a scalar (a number), not a vector. "
                "Geometrically: a·b = |a||b|cos φ, where φ is the angle between a and b."
            ),
            "formula": "a · b = |a| |b| cos φ",
        },
        {
            "id": "1",
            "title": "1. Coordinate formula",
            "explain": (
                "In ℝⁿ the dot product is computed coordinate-wise: "
                "sum the products of matching components."
            ),
            "formula": "a · b = a₁b₁ + a₂b₂ + … + aₙbₙ",
        },
        {
            "id": "2",
            "title": "2. Angle and cosine",
            "explain": (
                "If both vectors are nonzero, cos φ = (a·b)/(|a||b|). "
                "Acute φ ⟺ a·b > 0; obtuse ⟺ a·b < 0; right ⟺ a·b = 0."
            ),
            "formula": "cos φ = (a · b) / (|a| |b|)",
        },
        {
            "id": "3",
            "title": "3. Orthogonality",
            "explain": (
                "Vectors are perpendicular if and only if their dot product is zero: "
                "a ⊥ b ⟺ a·b = 0."
            ),
            "formula": "a ⊥ b  ⟺  a · b = 0",
        },
        {
            "id": "4",
            "title": "4. Projection onto b",
            "explain": (
                "The part of a along b is the orthogonal projection: "
                "proj_b(a) = ((a·b)/|b|²) b. The remainder a − proj_b(a) ⊥ b."
            ),
            "formula": "proj_b(a) = ((a·b) / |b|²) b",
        },
        {
            "id": "5",
            "title": "5. Properties",
            "explain": (
                "Commutative: a·b = b·a. Linear in each argument. "
                "Length: |a| = √(a·a). Identity: |a+b|² = |a|² + 2a·b + |b|²."
            ),
            "formula": "|a + b|² = |a|² + 2(a·b) + |b|²",
        },
        {
            "id": "6",
            "title": "6. Why it matters",
            "explain": (
                "The dot product underlies projections, angles, orthogonality in least squares, "
                "checking that residuals are perpendicular (v − proj ⊥ W), and physics (work W = F·d)."
            ),
            "formula": "work = F · d",
        },
    ],
    "skalyarnoe.stats.coords": "Coordinates:",
    "skalyarnoe.stats.orthogonal": "Orthogonal?  {ok}  (a·b = {val})",
    "skalyarnoe.stats.identity": "|a+b|² = {lhs},  |a|²+2a·b+|b|² = {rhs}  →  {ok}",
    "rang.page_title": "Matrix rank",
    "rang.preset.r22.label": "2×2, rank 2",
    "rang.preset.r22.hint": "Both columns independent — span = ℝ²",
    "rang.preset.r21.label": "2×2, rank 1",
    "rang.preset.r21.hint": "c₂ = 2c₁ — one-dimensional span",
    "rang.preset.r32.label": "3×2, rank 2",
    "rang.preset.r32.hint": "Two independent columns in ℝ³ — a plane",
    "rang.preset.r33.label": "3×3, rank 2",
    "rang.preset.r33.hint": "Third column = c₁ + c₂",
    "rang.steps": [
        {
            "id": "0",
            "title": "0. Definition of rank",
            "explain": (
                "The rank of matrix A is the dimension of the linear span of its columns "
                "(or rows). It is the maximum number of linearly independent columns."
            ),
            "formula": "rank(A) = dim Col(A) = dim Row(A)",
        },
        {
            "id": "1",
            "title": "1. Columns as vectors",
            "explain": (
                "An m×n matrix is n column vectors in ℝᵐ. "
                "Multiplication Ax is a linear combination of columns with coefficients from x."
            ),
            "formula": "Ax = x₁c₁ + x₂c₂ + … + xₙcₙ",
        },
        {
            "id": "2",
            "title": "2. Column space",
            "explain": (
                "Col(A) = span{c₁,…,cₙ} — all vectors obtainable "
                "as linear combinations of the columns."
            ),
            "formula": "Col(A) = { Ax : x ∈ ℝⁿ }",
        },
        {
            "id": "3",
            "title": "3. Independent columns",
            "explain": (
                "A column is dependent if it already lies in the span of previous pivot columns. "
                "Rank is the number of pivot (linearly independent) columns."
            ),
            "formula": "rank(A) = number of independent columns",
        },
        {
            "id": "4",
            "title": "4. Gaussian elimination",
            "explain": (
                "In row echelon form, rank equals the number of pivot (leading) entries. "
                "Dependent columns do not increase the dimension of the span."
            ),
            "formula": "rank(A) = number of nonzero pivot rows",
        },
        {
            "id": "5",
            "title": "5. Row and column rank",
            "explain": (
                "Fundamental theorem: row rank equals column rank. "
                "rank(A) = rank(Aᵀ)."
            ),
            "formula": "rank(A) = rank(Aᵀ)",
        },
        {
            "id": "6",
            "title": "6. Dimension and kernel",
            "explain": (
                "For m×n: rank(A) + nullity(A) = n, where nullity is the dimension of the kernel "
                "(solutions of Ax = 0). More column dependencies mean more free variables."
            ),
            "formula": "rank(A) + nullity(A) = n",
        },
        {
            "id": "7",
            "title": "7. Systems Ax = b",
            "explain": (
                "The system is consistent ⟺ rank(A) = rank([A|b]). "
                "Unique solution for square A ⟺ rank(A) = n; infinitely many when rank < n."
            ),
            "formula": "consistent ⟺ rank(A) = rank([A|b])",
        },
    ],
    "rang.stats.size": "Size: {rows}×{cols}",
    "rang.stats.rank": "rank(A) = {rank}",
    "rang.stats.nullity": "nullity(A) = {nullity}   (n − rank = {n} − {rank})",
    "rang.stats.columns": "Columns:",
    "rang.stats.col_pivot": "pivot",
    "rang.stats.col_dependent": "dependent",
    "rang.stats.rank_transpose": "rank(Aᵀ) = {rr}  (matches rank(A): {match})",
    "rang.stats.theorem": "Theorem: rank + nullity = {rank} + {nullity} = {n}",
    "rang.stats.systems": (
        "For Ax=b: if rank(A) < rank([A|b]) — no solution; "
        "if rank(A) = rank([A|b]) < n — infinitely many."
    ),
}

RU: dict = {
    "app.title": "Линейная алгебра",
    "home.subtitle": "Интерактивные визуализации. Выберите тему:",
    "home.footer": "Новые темы появятся здесь по мере добавления.",
    "home.open": "Открыть →",
    "nav.back": "← Все темы",
    "nav.btn_prev": "← Назад",
    "nav.btn_next": "Далее →",
    "section.plane": "Плоскость",
    "section.preset": "Пресет",
    "section.step": "Шаг",
    "section.explanation": "Пояснение",
    "section.matrix": "Матрица",
    "section.vector_v": "Вектор v",
    "section.vector_a": "Вектор a",
    "section.vector_b": "Вектор b",
    "topic.proekcia.title": "Проекция вектора на плоскость",
    "topic.proekcia.subtitle": "Пошаговый разбор формулы с интерактивным 3D-графиком.",
    "topic.proekcia.tag": "3D",
    "topic.skalyarnoe.title": "Скалярное произведение",
    "topic.skalyarnoe.subtitle": "Определение, угол, ортогональность и проекция на направление.",
    "topic.skalyarnoe.tag": "3D",
    "topic.rang.title": "Ранг матрицы",
    "topic.rang.subtitle": "Столбцы, линейная оболочка, независимость и теорема о ранге.",
    "topic.rang.tag": "3D",
    "proekcia.page_title": "Проекция",
    "proekcia.preset.xy.label": "1 — плоскость xy",
    "proekcia.preset.xy.hint": "Ортогональный базис: остаток строго вдоль z",
    "proekcia.preset.tilted.label": "2 — наклонная плоскость",
    "proekcia.preset.tilted.hint": "a₁ и a₂ не ортогональны — используйте (AᵀA)⁻¹Aᵀv",
    "proekcia.preset.general.label": "3 — общий v",
    "proekcia.preset.general.hint": "Типичный случай: v вне плоскости",
    "proekcia.steps": [
        {
            "id": "0",
            "title": "0. Плоскость W и базис u₁, u₂",
            "explain": "W — плоскость. u₁ и u₂ — ортонормированные векторы в W (uᵢ·uⱼ = 0, |uᵢ| = 1).",
            "formula": "proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂",
        },
        {
            "id": "1",
            "title": "1. Скаляр v·u₁",
            "explain": "v·u₁ — знаковая длина «тени» v на ось u₁, коэффициент вдоль u₁.",
            "formula": "v·u₁ = ?",
        },
        {
            "id": "2",
            "title": "2. Вектор (v·u₁)u₁",
            "explain": "Умножаем единичный u₁ на скаляр — получаем составляющую v вдоль u₁.",
            "formula": "(v·u₁)u₁",
        },
        {
            "id": "3",
            "title": "3. Скаляр v·u₂",
            "explain": "То же для второго направления: скалярная проекция на u₂.",
            "formula": "v·u₂ = ?",
        },
        {
            "id": "4",
            "title": "4. Вектор (v·u₂)u₂",
            "explain": "Вторая составляющая — часть v вдоль u₂, лежащая в плоскости W.",
            "formula": "(v·u₂)u₂",
        },
        {
            "id": "5",
            "title": "5. Сумма = proj_W(v)",
            "explain": "Складываем обе составляющие — проекция v на всю плоскость W.",
            "formula": "(v·u₁)u₁ + (v·u₂)u₂ = proj_W(v)",
        },
        {
            "id": "6",
            "title": "6. Остаток v − proj",
            "explain": "Разность v − proj ортогональна плоскости: остаток ⊥ u₁ и ⊥ u₂.",
            "formula": "v = proj_W(v) + (v − proj_W(v))",
        },
    ],
    "proekcia.stats.header": "Формула:  proj_W(v) = (v·u₁)u₁ + (v·u₂)u₂",
    "proekcia.stats.check": "Проверка: comp₁ + comp₂ = proj ?  {ok}",
    "skalyarnoe.page_title": "Скалярное произведение",
    "skalyarnoe.preset.acute.label": "Острый угол",
    "skalyarnoe.preset.acute.hint": "a·b > 0, cos φ > 0",
    "skalyarnoe.preset.right.label": "Прямой угол",
    "skalyarnoe.preset.right.hint": "a ⊥ b, a·b = 0",
    "skalyarnoe.preset.obtuse.label": "Тупой угол",
    "skalyarnoe.preset.obtuse.hint": "a·b < 0",
    "skalyarnoe.preset.parallel.label": "Параллельные",
    "skalyarnoe.preset.parallel.hint": "b = 2a, cos φ = 1",
    "skalyarnoe.steps": [
        {
            "id": "0",
            "title": "0. Определение",
            "explain": (
                "Скалярное произведение двух векторов — число (скаляр), а не вектор. "
                "Геометрически: a·b = |a||b|cos φ, где φ — угол между a и b."
            ),
            "formula": "a · b = |a| |b| cos φ",
        },
        {
            "id": "1",
            "title": "1. Координатная формула",
            "explain": (
                "В ℝⁿ скалярное произведение считают по координатам: "
                "сумма произведений одноимённых компонент."
            ),
            "formula": "a · b = a₁b₁ + a₂b₂ + … + aₙbₙ",
        },
        {
            "id": "2",
            "title": "2. Угол и косинус",
            "explain": (
                "Если оба вектора ненулевые, cos φ = (a·b)/(|a||b|). "
                "Острый φ ⟺ a·b > 0; тупой ⟺ a·b < 0; прямой ⟺ a·b = 0."
            ),
            "formula": "cos φ = (a · b) / (|a| |b|)",
        },
        {
            "id": "3",
            "title": "3. Ортогональность",
            "explain": (
                "Векторы перпендикулярны тогда и только тогда, когда их скалярное произведение ноль: "
                "a ⊥ b ⟺ a·b = 0."
            ),
            "formula": "a ⊥ b  ⟺  a · b = 0",
        },
        {
            "id": "4",
            "title": "4. Проекция на b",
            "explain": (
                "Часть a вдоль b — ортогональная проекция: "
                "proj_b(a) = ((a·b)/|b|²) b. Остаток a − proj_b(a) ⊥ b."
            ),
            "formula": "proj_b(a) = ((a·b) / |b|²) b",
        },
        {
            "id": "5",
            "title": "5. Свойства",
            "explain": (
                "Коммутативность: a·b = b·a. Линейность по каждому аргументу. "
                "Длина: |a| = √(a·a). Тождество: |a+b|² = |a|² + 2a·b + |b|²."
            ),
            "formula": "|a + b|² = |a|² + 2(a·b) + |b|²",
        },
        {
            "id": "6",
            "title": "6. Зачем это нужно",
            "explain": (
                "Скалярное произведение лежит в основе проекций, углов, ортогональности в МНК, "
                "проверки ⊥ остатка (v − proj ⊥ W) и физики (работа W = F·d)."
            ),
            "formula": "работа = F · d",
        },
    ],
    "skalyarnoe.stats.coords": "Координаты:",
    "skalyarnoe.stats.orthogonal": "Ортогональны?  {ok}  (a·b = {val})",
    "skalyarnoe.stats.identity": "|a+b|² = {lhs},  |a|²+2a·b+|b|² = {rhs}  →  {ok}",
    "rang.page_title": "Ранг матрицы",
    "rang.preset.r22.label": "2×2, ранг 2",
    "rang.preset.r22.hint": "Оба столбца независимы — оболочка = ℝ²",
    "rang.preset.r21.label": "2×2, ранг 1",
    "rang.preset.r21.hint": "c₂ = 2c₁ — одномерная оболочка",
    "rang.preset.r32.label": "3×2, ранг 2",
    "rang.preset.r32.hint": "Два независимых столбца в ℝ³ — плоскость",
    "rang.preset.r33.label": "3×3, ранг 2",
    "rang.preset.r33.hint": "Третий столбец = c₁ + c₂",
    "rang.steps": [
        {
            "id": "0",
            "title": "0. Определение ранга",
            "explain": (
                "Ранг матрицы A — размерность линейной оболочки её столбцов "
                "(или строк). Это максимальное число линейно независимых столбцов."
            ),
            "formula": "rank(A) = dim Col(A) = dim Row(A)",
        },
        {
            "id": "1",
            "title": "1. Столбцы как векторы",
            "explain": (
                "Матрица m×n — это n столбцов-векторов в ℝᵐ. "
                "Умножение Ax — линейная комбинация столбцов с коэффициентами из x."
            ),
            "formula": "Ax = x₁c₁ + x₂c₂ + … + xₙcₙ",
        },
        {
            "id": "2",
            "title": "2. Столбцовое пространство",
            "explain": (
                "Col(A) = span{c₁,…,cₙ} — все векторы, получаемые "
                "линейными комбинациями столбцов."
            ),
            "formula": "Col(A) = { Ax : x ∈ ℝⁿ }",
        },
        {
            "id": "3",
            "title": "3. Независимые столбцы",
            "explain": (
                "Столбец зависим, если уже лежит в оболочке предыдущих ведущих столбцов. "
                "Ранг — число ведущих (линейно независимых) столбцов."
            ),
            "formula": "rank(A) = число независимых столбцов",
        },
        {
            "id": "4",
            "title": "4. Метод Гаусса",
            "explain": (
                "В ступенчатом виде ранг равен числу ведущих (главных) элементов. "
                "Зависимые столбцы не увеличивают размерность оболочки."
            ),
            "formula": "rank(A) = число ненулевых ведущих строк",
        },
        {
            "id": "5",
            "title": "5. Ранг строк и столбцов",
            "explain": (
                "Фундаментальная теорема: ранг по строкам равен рангу по столбцам. "
                "rank(A) = rank(Aᵀ)."
            ),
            "formula": "rank(A) = rank(Aᵀ)",
        },
        {
            "id": "6",
            "title": "6. Размерность и ядро",
            "explain": (
                "Для m×n: rank(A) + nullity(A) = n, где nullity — размерность ядра "
                "(решений Ax = 0). Больше зависимостей столбцов — больше свободных переменных."
            ),
            "formula": "rank(A) + nullity(A) = n",
        },
        {
            "id": "7",
            "title": "7. Системы Ax = b",
            "explain": (
                "Система совместна ⟺ rank(A) = rank([A|b]). "
                "Единственное решение для квадратной A ⟺ rank(A) = n; бесконечно много при rank < n."
            ),
            "formula": "совместна ⟺ rank(A) = rank([A|b])",
        },
    ],
    "rang.stats.size": "Размер: {rows}×{cols}",
    "rang.stats.rank": "rank(A) = {rank}",
    "rang.stats.nullity": "nullity(A) = {nullity}   (n − rank = {n} − {rank})",
    "rang.stats.columns": "Столбцы:",
    "rang.stats.col_pivot": "ведущий",
    "rang.stats.col_dependent": "зависимый",
    "rang.stats.rank_transpose": "rank(Aᵀ) = {rr}  (совпадает с rank(A): {match})",
    "rang.stats.theorem": "Теорема: rank + nullity = {rank} + {nullity} = {n}",
    "rang.stats.systems": (
        "Для Ax=b: если rank(A) < rank([A|b]) — нет решений; "
        "если rank(A) = rank([A|b]) < n — бесконечно много."
    ),
}

MESSAGES: dict[str, dict] = {"en": EN, "ru": RU}

# Preset id lists per topic (stable keys for dropdown values)
PRESET_IDS: dict[str, tuple[str, ...]] = {
    "proekcia": ("xy", "tilted", "general"),
    "skalyarnoe": ("acute", "right", "obtuse", "parallel"),
    "rang": ("r22", "r21", "r32", "r33"),
}
