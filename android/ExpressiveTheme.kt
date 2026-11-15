// Expressive Kit, generated from tokens/tokens.json by scripts/build.py. Do not edit by hand.
// Fonts: add Google Sans Flex, Fraunces and Google Sans Code as res/font files (or downloadable fonts),
// then pass them to expressiveTypography(), e.g.
//   expressiveTypography(sans = { size -> variableFontFamily(R.font.google_sans_flex, size) })
// Requires androidx.compose.material3 1.4 or later for MaterialExpressiveTheme and MotionScheme.
@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

package design.expressive.kit

import android.os.Build
import androidx.annotation.FontRes
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ColorScheme
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.LocalTonalElevationEnabled
import androidx.compose.material3.MaterialExpressiveTheme
import androidx.compose.material3.MotionScheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.dynamicDarkColorScheme
import androidx.compose.material3.dynamicLightColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.lerp
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.Font
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontVariation
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val SansFamily: FontFamily = FontFamily.SansSerif
val DisplayFamily: FontFamily = FontFamily.Serif
val MonoFamily: FontFamily = FontFamily.Monospace

private val familyCache = HashMap<Pair<Int, Int>, FontFamily>()

/**
 * A variable font pinned to one optical size, with real cuts at each weight.
 *
 * M3 type tokens set the `opsz` axis equal to the font size, so small text gets the sturdier
 * text cut and large text the tighter display cut from one font file. Pass the result to
 * [expressiveTypography] per size.
 */
fun variableFontFamily(
    @FontRes resId: Int,
    opticalSize: Float,
    weights: IntArray = intArrayOf(400, 500, 600, 700, 800),
): FontFamily = familyCache.getOrPut(resId to opticalSize.toInt()) {
    FontFamily(
        weights.map { w ->
            Font(
                resId = resId,
                weight = FontWeight(w),
                variationSettings = FontVariation.Settings(
                    FontVariation.weight(w),
                    FontVariation.Setting("opsz", opticalSize.coerceIn(6f, 144f)),
                ),
            )
        },
    )
}

val ExpressiveLightColors = lightColorScheme(
    primary = Color(0xFFA8330F),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFFFFDBCF),
    onPrimaryContainer = Color(0xFF3B0900),
    inversePrimary = Color(0xFFFFB59C),
    secondary = Color(0xFF2C6765),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFBDEEEA),
    onSecondaryContainer = Color(0xFF00201F),
    tertiary = Color(0xFF7A4E8F),
    onTertiary = Color(0xFFFFFFFF),
    tertiaryContainer = Color(0xFFF3DAFF),
    onTertiaryContainer = Color(0xFF2F0A44),
    surface = Color(0xFFFBF6EE),
    onSurface = Color(0xFF1F1A16),
    onSurfaceVariant = Color(0xFF54463D),
    inverseSurface = Color(0xFF362F2B),
    inverseOnSurface = Color(0xFFFBEEE8),
    error = Color(0xFFBA1A1A),
    onError = Color(0xFFFFFFFF),
    errorContainer = Color(0xFFFFDAD6),
    onErrorContainer = Color(0xFF410002),
    outline = Color(0xFF85736A),
    outlineVariant = Color(0xFFD9C7BC),
    surfaceContainerLowest = Color(0xFFFFFFFF),
    surfaceContainerLow = Color(0xFFF6EFE6),
    surfaceContainer = Color(0xFFF1E9DF),
    surfaceContainerHigh = Color(0xFFEBE2D6),
    surfaceContainerHighest = Color(0xFFE4DACD),
    background = Color(0xFFFBF6EE),
    onBackground = Color(0xFF1F1A16),
    scrim = Color(0x66140C08),
)

val ExpressiveDarkColors = darkColorScheme(
    primary = Color(0xFFFFB59C),
    onPrimary = Color(0xFF5C1900),
    primaryContainer = Color(0xFF7C2A0E),
    onPrimaryContainer = Color(0xFFFFDBCF),
    inversePrimary = Color(0xFFA8330F),
    secondary = Color(0xFF97D1CE),
    onSecondary = Color(0xFF003735),
    secondaryContainer = Color(0xFF1D4E4C),
    onSecondaryContainer = Color(0xFFBDEEEA),
    tertiary = Color(0xFFE3B6FB),
    onTertiary = Color(0xFF46205A),
    tertiaryContainer = Color(0xFF5B3A6C),
    onTertiaryContainer = Color(0xFFF3DAFF),
    surface = Color(0xFF1A1210),
    onSurface = Color(0xFFF0E1D9),
    onSurfaceVariant = Color(0xFFD8C3B8),
    inverseSurface = Color(0xFFF0E1D9),
    inverseOnSurface = Color(0xFF362F2B),
    error = Color(0xFFFFB4AB),
    onError = Color(0xFF690005),
    errorContainer = Color(0xFF93000A),
    onErrorContainer = Color(0xFFFFDAD6),
    outline = Color(0xFFA28E85),
    outlineVariant = Color(0xFF54453E),
    surfaceContainerLowest = Color(0xFF140D0B),
    surfaceContainerLow = Color(0xFF221815),
    surfaceContainer = Color(0xFF271D19),
    surfaceContainerHigh = Color(0xFF322723),
    surfaceContainerHighest = Color(0xFF3D312C),
    background = Color(0xFF1A1210),
    onBackground = Color(0xFFF0E1D9),
    scrim = Color(0x8F000000),
)

/** Roles Material 3 has no slot for: the loud highlight fill and gain/success colours. */
@Immutable
data class ExtendedColors(
    val highlight: Color,
    val onHighlight: Color,
    val positive: Color,
    val positiveContainer: Color,
    val onPositiveContainer: Color,
)

val ExpressiveLightExtended = ExtendedColors(
    highlight = Color(0xFFFC9500),
    onHighlight = Color(0xFF2B1700),
    positive = Color(0xFF1B6D3B),
    positiveContainer = Color(0xFFC3EFCF),
    onPositiveContainer = Color(0xFF00210C),
)

val ExpressiveDarkExtended = ExtendedColors(
    highlight = Color(0xFFFFB84D),
    onHighlight = Color(0xFF2B1700),
    positive = Color(0xFF7FD9A3),
    positiveContainer = Color(0xFF0F4A28),
    onPositiveContainer = Color(0xFFC3EFCF),
)

val LocalExtendedColors = staticCompositionLocalOf { ExpressiveLightExtended }

/**
 * True-black variant of a dark scheme for OLED screens. The page goes black and the low
 * containers darken, so cards on `surfaceContainer` and above separate more, not less.
 */
fun ColorScheme.toAmoledBlack(): ColorScheme = copy(
    background = Color.Black,
    surface = Color.Black,
    surfaceDim = Color.Black,
    surfaceContainerLowest = Color.Black,
    surfaceContainerLow = lerp(surfaceContainerLow, Color.Black, 0.6f),
    surfaceContainer = lerp(surfaceContainer, Color.Black, 0.35f),
    scrim = Color.Black,
)

val ExpressiveShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    largeIncreased = RoundedCornerShape(20.dp),
    extraLarge = RoundedCornerShape(28.dp),
    extraLargeIncreased = RoundedCornerShape(32.dp),
    extraExtraLarge = RoundedCornerShape(48.dp),
)

/**
 * The type scale with all fifteen emphasized twins. Each family lambda receives the style's
 * font size so a variable font can pin its optical size to it (see [variableFontFamily]).
 */
fun expressiveTypography(
    sans: (Float) -> FontFamily = { SansFamily },
    display: (Float) -> FontFamily = { DisplayFamily },
): Typography {
    return Typography(
        displayLarge = TextStyle(fontFamily = display(57f), fontSize = 57.sp, lineHeight = 64.sp, fontWeight = FontWeight(600), letterSpacing = (-0.5).sp),
        displayMedium = TextStyle(fontFamily = display(45f), fontSize = 45.sp, lineHeight = 52.sp, fontWeight = FontWeight(600), letterSpacing = (-0.25).sp),
        displaySmall = TextStyle(fontFamily = display(36f), fontSize = 36.sp, lineHeight = 44.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
        headlineLarge = TextStyle(fontFamily = sans(32f), fontSize = 32.sp, lineHeight = 40.sp, fontWeight = FontWeight(700), letterSpacing = (-0.5).sp),
        headlineMedium = TextStyle(fontFamily = sans(28f), fontSize = 28.sp, lineHeight = 36.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
        headlineSmall = TextStyle(fontFamily = sans(24f), fontSize = 24.sp, lineHeight = 32.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
        titleLarge = TextStyle(fontFamily = sans(22f), fontSize = 22.sp, lineHeight = 28.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
        titleMedium = TextStyle(fontFamily = sans(16f), fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
        titleSmall = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
        bodyLarge = TextStyle(fontFamily = sans(16f), fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(400), letterSpacing = (0).sp),
        bodyMedium = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(400), letterSpacing = (0.25).sp),
        bodySmall = TextStyle(fontFamily = sans(12f), fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(400), letterSpacing = (0.4).sp),
        labelLarge = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
        labelMedium = TextStyle(fontFamily = sans(12f), fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(600), letterSpacing = (0.5).sp),
        labelSmall = TextStyle(fontFamily = sans(11f), fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight(600), letterSpacing = (0.5).sp),
        displayLargeEmphasized = TextStyle(fontFamily = display(57f), fontSize = 57.sp, lineHeight = 64.sp, fontWeight = FontWeight(700), letterSpacing = (-0.5).sp),
        displayMediumEmphasized = TextStyle(fontFamily = display(45f), fontSize = 45.sp, lineHeight = 52.sp, fontWeight = FontWeight(700), letterSpacing = (-0.25).sp),
        displaySmallEmphasized = TextStyle(fontFamily = display(36f), fontSize = 36.sp, lineHeight = 44.sp, fontWeight = FontWeight(700), letterSpacing = (0).sp),
        headlineLargeEmphasized = TextStyle(fontFamily = sans(32f), fontSize = 32.sp, lineHeight = 40.sp, fontWeight = FontWeight(800), letterSpacing = (-0.5).sp),
        headlineMediumEmphasized = TextStyle(fontFamily = sans(28f), fontSize = 28.sp, lineHeight = 36.sp, fontWeight = FontWeight(700), letterSpacing = (0).sp),
        headlineSmallEmphasized = TextStyle(fontFamily = sans(24f), fontSize = 24.sp, lineHeight = 32.sp, fontWeight = FontWeight(700), letterSpacing = (0).sp),
        titleLargeEmphasized = TextStyle(fontFamily = sans(22f), fontSize = 22.sp, lineHeight = 28.sp, fontWeight = FontWeight(700), letterSpacing = (0).sp),
        titleMediumEmphasized = TextStyle(fontFamily = sans(16f), fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(700), letterSpacing = (0.1).sp),
        titleSmallEmphasized = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(700), letterSpacing = (0.1).sp),
        bodyLargeEmphasized = TextStyle(fontFamily = sans(16f), fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(500), letterSpacing = (0).sp),
        bodyMediumEmphasized = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(500), letterSpacing = (0.25).sp),
        bodySmallEmphasized = TextStyle(fontFamily = sans(12f), fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(500), letterSpacing = (0.4).sp),
        labelLargeEmphasized = TextStyle(fontFamily = sans(14f), fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(700), letterSpacing = (0.1).sp),
        labelMediumEmphasized = TextStyle(fontFamily = sans(12f), fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(700), letterSpacing = (0.5).sp),
        labelSmallEmphasized = TextStyle(fontFamily = sans(11f), fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight(700), letterSpacing = (0.5).sp),
    )
}

val ExpressiveTypography = expressiveTypography()

/** Styles beyond the Material type scale: hero numerals and mono data labels. */
object ExpressiveTextStyles {
    val numeralLarge = TextStyle(fontFamily = SansFamily, fontSize = 56.sp, lineHeight = 60.sp, fontWeight = FontWeight(700), letterSpacing = (-1.5).sp)
    val numeralMedium = TextStyle(fontFamily = SansFamily, fontSize = 40.sp, lineHeight = 44.sp, fontWeight = FontWeight(700), letterSpacing = (-1).sp)
    val numeralSmall = TextStyle(fontFamily = SansFamily, fontSize = 28.sp, lineHeight = 32.sp, fontWeight = FontWeight(700), letterSpacing = (-0.5).sp)
    val eyebrow = TextStyle(fontFamily = MonoFamily, fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight(500), letterSpacing = (1.2).sp)
    val dataMedium = TextStyle(fontFamily = MonoFamily, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(500), letterSpacing = (0).sp)
    val dataSmall = TextStyle(fontFamily = MonoFamily, fontSize = 11.sp, lineHeight = 14.sp, fontWeight = FontWeight(500), letterSpacing = (0.3).sp)
}

/**
 * The Expressive Kit theme.
 *
 * Uses [MaterialExpressiveTheme], which installs the expressive motion scheme, shapes and
 * emphasized type. Motion tokens map onto the scheme's springs (damping ratio / stiffness):
 *   spatial-fast     expressive 0.6 / 800   standard 0.9 / 1400  -> MaterialTheme.motionScheme.fastSpatialSpec()
 *   spatial-default  expressive 0.8 / 380   standard 0.9 / 700   -> MaterialTheme.motionScheme.defaultSpatialSpec()
 *   spatial-slow     expressive 0.8 / 200   standard 0.9 / 300   -> MaterialTheme.motionScheme.slowSpatialSpec()
 *   effects-fast     expressive 1.0 / 3800  standard 1.0 / 3800  -> MaterialTheme.motionScheme.fastEffectsSpec()
 *   effects-default  expressive 1.0 / 1600  standard 1.0 / 1600  -> MaterialTheme.motionScheme.defaultEffectsSpec()
 *   effects-slow     expressive 1.0 / 800   standard 1.0 / 800   -> MaterialTheme.motionScheme.slowEffectsSpec()
 * Read them from `MaterialTheme.motionScheme` rather than hard-coding springs.
 *
 * @param motionScheme [MotionScheme.expressive] for consumer and playful apps (overshoot), or
 *   [MotionScheme.standard] for productivity and utility apps (no visible bounce).
 * @param dynamicColor derive colours from the wallpaper on Android 12+. Off by default so the
 *   brand palette shows; keep brand moments (hero cards, illustrations) on brand colours either way.
 * @param amoledBlack in dark theme, use a true-black page for OLED screens.
 */
@Composable
fun ExpressiveTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    motionScheme: MotionScheme = MotionScheme.expressive(),
    dynamicColor: Boolean = false,
    amoledBlack: Boolean = false,
    typography: Typography = ExpressiveTypography,
    content: @Composable () -> Unit,
) {
    val context = LocalContext.current
    val base = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S ->
            if (darkTheme) dynamicDarkColorScheme(context) else dynamicLightColorScheme(context)
        darkTheme -> ExpressiveDarkColors
        else -> ExpressiveLightColors
    }
    val amoled = darkTheme && amoledBlack
    val colorScheme = remember(base, amoled) { if (amoled) base.toAmoledBlack() else base }
    CompositionLocalProvider(
        LocalExtendedColors provides if (darkTheme) ExpressiveDarkExtended else ExpressiveLightExtended,
        // Tonal elevation would paint grey back over a true-black page.
        LocalTonalElevationEnabled provides !amoled,
    ) {
        MaterialExpressiveTheme(
            colorScheme = colorScheme,
            motionScheme = motionScheme,
            shapes = ExpressiveShapes,
            typography = typography,
            content = content,
        )
    }
}

object Expressive {
    val extendedColors: ExtendedColors
        @Composable get() = LocalExtendedColors.current
}
