// Expressive Kit, generated from tokens/tokens.json by scripts/build.py. Do not edit by hand.
// Fonts: add Google Sans Flex, Fraunces and Google Sans Code with downloadable fonts
// (androidx.compose.ui:ui-text-google-fonts) or as res/font files, then replace the families below.
package design.expressive.kit

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Shapes
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

val SansFamily: FontFamily = FontFamily.SansSerif
val DisplayFamily: FontFamily = FontFamily.Serif
val MonoFamily: FontFamily = FontFamily.Monospace

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

val ExpressiveShapes = Shapes(
    extraSmall = RoundedCornerShape(4.dp),
    small = RoundedCornerShape(8.dp),
    medium = RoundedCornerShape(12.dp),
    large = RoundedCornerShape(16.dp),
    extraLarge = RoundedCornerShape(28.dp),
)

val ExpressiveTypography = Typography(
    displayLarge = TextStyle(fontFamily = DisplayFamily, fontSize = 57.sp, lineHeight = 64.sp, fontWeight = FontWeight(600), letterSpacing = (-0.5).sp),
    displayMedium = TextStyle(fontFamily = DisplayFamily, fontSize = 45.sp, lineHeight = 52.sp, fontWeight = FontWeight(600), letterSpacing = (-0.25).sp),
    displaySmall = TextStyle(fontFamily = DisplayFamily, fontSize = 36.sp, lineHeight = 44.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
    headlineLarge = TextStyle(fontFamily = SansFamily, fontSize = 32.sp, lineHeight = 40.sp, fontWeight = FontWeight(700), letterSpacing = (-0.5).sp),
    headlineMedium = TextStyle(fontFamily = SansFamily, fontSize = 28.sp, lineHeight = 36.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
    headlineSmall = TextStyle(fontFamily = SansFamily, fontSize = 24.sp, lineHeight = 32.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
    titleLarge = TextStyle(fontFamily = SansFamily, fontSize = 22.sp, lineHeight = 28.sp, fontWeight = FontWeight(600), letterSpacing = (0).sp),
    titleMedium = TextStyle(fontFamily = SansFamily, fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
    titleSmall = TextStyle(fontFamily = SansFamily, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
    bodyLarge = TextStyle(fontFamily = SansFamily, fontSize = 16.sp, lineHeight = 24.sp, fontWeight = FontWeight(400), letterSpacing = (0).sp),
    bodyMedium = TextStyle(fontFamily = SansFamily, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(400), letterSpacing = (0.25).sp),
    bodySmall = TextStyle(fontFamily = SansFamily, fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(400), letterSpacing = (0.4).sp),
    labelLarge = TextStyle(fontFamily = SansFamily, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(600), letterSpacing = (0.1).sp),
    labelMedium = TextStyle(fontFamily = SansFamily, fontSize = 12.sp, lineHeight = 16.sp, fontWeight = FontWeight(600), letterSpacing = (0.5).sp),
    labelSmall = TextStyle(fontFamily = SansFamily, fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight(600), letterSpacing = (0.5).sp),
)

/** Styles beyond the Material type scale: hero numerals and mono data labels. */
object ExpressiveTextStyles {
    val numeralLarge = TextStyle(fontFamily = SansFamily, fontSize = 56.sp, lineHeight = 60.sp, fontWeight = FontWeight(700), letterSpacing = (-1.5).sp)
    val numeralMedium = TextStyle(fontFamily = SansFamily, fontSize = 40.sp, lineHeight = 44.sp, fontWeight = FontWeight(700), letterSpacing = (-1).sp)
    val numeralSmall = TextStyle(fontFamily = SansFamily, fontSize = 28.sp, lineHeight = 32.sp, fontWeight = FontWeight(700), letterSpacing = (-0.5).sp)
    val eyebrow = TextStyle(fontFamily = MonoFamily, fontSize = 11.sp, lineHeight = 16.sp, fontWeight = FontWeight(500), letterSpacing = (1.2).sp)
    val dataMedium = TextStyle(fontFamily = MonoFamily, fontSize = 14.sp, lineHeight = 20.sp, fontWeight = FontWeight(500), letterSpacing = (0).sp)
    val dataSmall = TextStyle(fontFamily = MonoFamily, fontSize = 11.sp, lineHeight = 14.sp, fontWeight = FontWeight(500), letterSpacing = (0.3).sp)
}

@Composable
fun ExpressiveTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    CompositionLocalProvider(LocalExtendedColors provides if (darkTheme) ExpressiveDarkExtended else ExpressiveLightExtended) {
        MaterialTheme(
            colorScheme = if (darkTheme) ExpressiveDarkColors else ExpressiveLightColors,
            shapes = ExpressiveShapes,
            typography = ExpressiveTypography,
            content = content,
        )
    }
}

object Expressive {
    val extendedColors: ExtendedColors
        @Composable get() = LocalExtendedColors.current
}
