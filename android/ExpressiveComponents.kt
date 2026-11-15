// Expressive Kit components that Material 3 Compose does not ship. Hand-written; the web versions
// live in components/RotaryDial and components/TimePickerDial. Uses ExpressiveMotion.kt for springs,
// haptics and reduced motion.
@file:OptIn(ExperimentalMaterial3ExpressiveApi::class)

package design.expressive.kit

import androidx.compose.animation.core.Animatable
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.draggable
import androidx.compose.foundation.gestures.rememberDraggableState
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.ExperimentalMaterial3ExpressiveApi
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.onSizeChanged
import androidx.compose.ui.semantics.ProgressBarRangeInfo
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.progressBarRangeInfo
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.semantics.setProgress
import androidx.compose.ui.semantics.stateDescription
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.atan2
import kotlin.math.ceil
import kotlin.math.cos
import kotlin.math.roundToInt
import kotlin.math.sin

/**
 * A drum you turn to set a value, drawn edge-on in perspective with the slider's anatomy: the drum
 * is the track (`surfaceContainerHighest`) and the graduation under the centre turns `primary` and
 * acts as the handle. Drag or fling; on release it snaps with the fast spatial spring and keeps the
 * fling's velocity. Each step that passes the centre ticks a haptic.
 *
 * The drag accumulates in a float and the drawing follows that float, not the rounded value, and the
 * control ignores its own echo of [value], so the drum never jumps back to a whole number mid-drag.
 */
@Composable
fun RotaryDial(
    value: Int,
    onValueChange: (Int) -> Unit,
    range: IntRange,
    modifier: Modifier = Modifier,
    contentDescription: String = "",
    height: Dp = 76.dp,
    stepRadians: Float = 0.08f,
    majorEvery: Int = 5,
) {
    val haptic = rememberHaptics()
    val scope = rememberCoroutineScope()
    val position = remember { Animatable(value.toFloat()) }
    var dragPosition by remember { mutableFloatStateOf(value.toFloat()) }
    var dragging by remember { mutableStateOf(false) }
    var lastEmitted by remember { mutableIntStateOf(value) }
    var widthPx by remember { mutableFloatStateOf(1f) }
    val snap = MaterialTheme.motionScheme.fastSpatialSpec<Float>()
    val settle = MaterialTheme.motionScheme.defaultSpatialSpec<Float>()
    val currentOnChange by rememberUpdatedState(onValueChange)
    val track = MaterialTheme.colorScheme.surfaceContainerHighest
    val ridge = MaterialTheme.colorScheme.onSurfaceVariant
    val accent = MaterialTheme.colorScheme.primary
    val lo = range.first.toFloat()
    val hi = range.last.toFloat()

    // Only a genuinely external change re-seats the drum.
    LaunchedEffect(value) {
        if (value != lastEmitted) {
            lastEmitted = value
            position.animateTo(value.toFloat(), settle)
        }
    }

    fun emit(v: Float) {
        val stepped = v.roundToInt().coerceIn(range)
        if (stepped != lastEmitted) {
            lastEmitted = stepped
            haptic(ExpressiveHaptic.Tick)
            currentOnChange(stepped)
        }
    }

    fun pxPerStep() = (widthPx / 2f - 8f) * stepRadians

    Canvas(
        modifier
            .fillMaxWidth()
            .height(height)
            .clip(RoundedCornerShape(18.dp))
            .background(track)
            .onSizeChanged { widthPx = it.width.toFloat() }
            .semantics {
                this.contentDescription = contentDescription
                stateDescription = value.toString()
                progressBarRangeInfo = ProgressBarRangeInfo(value.toFloat(), lo..hi, steps = (range.last - range.first - 1).coerceAtLeast(0))
                setProgress { target ->
                    val stepped = target.roundToInt().coerceIn(range)
                    scope.launch { position.animateTo(stepped.toFloat(), snap) }
                    emit(stepped.toFloat())
                    true
                }
            }
            .draggable(
                orientation = Orientation.Horizontal,
                state = rememberDraggableState { delta ->
                    dragPosition = (dragPosition - delta / pxPerStep()).coerceIn(lo, hi)
                    emit(dragPosition)
                },
                onDragStarted = {
                    position.stop()
                    dragPosition = position.value
                    dragging = true
                },
                onDragStopped = { velocity ->
                    position.snapTo(dragPosition)
                    dragging = false
                    val stepsPerSecond = -velocity / pxPerStep()
                    val target = (dragPosition + stepsPerSecond * 0.12f).roundToInt().coerceIn(range)
                    position.animateTo(target.toFloat(), snap, initialVelocity = stepsPerSecond)
                    emit(target.toFloat())
                },
            ),
    ) {
        val pos = if (dragging) dragPosition else position.value
        val radius = size.width / 2f - 8.dp.toPx()
        val centreX = size.width / 2f
        val visible = ceil((PI / 2) / stepRadians).toInt()
        val centre = pos.roundToInt()
        for (i in (centre - visible)..(centre + visible)) {
            if (i < range.first || i > range.last) continue
            val theta = (i - pos) * stepRadians
            if (abs(theta) >= PI / 2) continue
            val depth = cos(theta)
            val major = i % majorEvery == 0
            val near = abs(i - pos) < 0.5f
            val w = (1f + depth * (if (major) 2.2f else 1.4f)).dp.toPx()
            val h = size.height * (if (major) 0.46f else 0.3f)
            drawRoundRect(
                color = if (near) accent else ridge.copy(alpha = 0.18f + 0.7f * depth * depth),
                topLeft = Offset(centreX + radius * sin(theta) - w / 2f, (size.height - h) / 2f),
                size = Size(w, h),
                cornerRadius = CornerRadius(w / 2f),
            )
        }
        drawCircle(accent, radius = 3.dp.toPx(), center = Offset(centreX, size.height - 9.dp.toPx()))
    }
}

/**
 * A 12-hour clock dial for picking an hour or minutes. The handle springs to a tapped number by the
 * short way round and follows the finger exactly while dragging; each change ticks a haptic. Lifting
 * the finger in hour mode calls [onHourPicked] so the caller can switch to minutes.
 *
 * For most forms prefer Material 3's `TimePicker(state)`; use this when the dial is the hero of the
 * screen (an alarm or timer app) and must match a custom face.
 */
@Composable
fun TimeDial(
    hour: Int,
    minute: Int,
    selectingMinutes: Boolean,
    onChange: (hour: Int, minute: Int) -> Unit,
    modifier: Modifier = Modifier,
    onHourPicked: () -> Unit = {},
) {
    val haptic = rememberHaptics()
    val measurer = rememberTextMeasurer()
    val labelStyle = MaterialTheme.typography.bodyLarge
    val face = MaterialTheme.colorScheme.surfaceContainerHighest
    val ink = MaterialTheme.colorScheme.onSurface
    val accent = MaterialTheme.colorScheme.primary
    val onAccent = MaterialTheme.colorScheme.onPrimary
    val spring = MaterialTheme.motionScheme.fastSpatialSpec<Float>()
    val currentOnChange by rememberUpdatedState(onChange)
    val currentHourPicked by rememberUpdatedState(onHourPicked)
    val pm = hour >= 12

    val targetAngle = if (selectingMinutes) minute * 6f else (hour % 12) * 30f
    val angle = remember { Animatable(targetAngle) }
    var dragging by remember { mutableStateOf(false) }
    LaunchedEffect(targetAngle, dragging) {
        // Shortest path: 330 -> 0 turns forward to 360, then re-bases.
        val delta = ((targetAngle - angle.value) % 360f + 540f) % 360f - 180f
        if (dragging) angle.snapTo(angle.value + delta) else angle.animateTo(angle.value + delta, spring)
    }

    fun pick(position: Offset, sizePx: Float) {
        val x = position.x - sizePx / 2f
        val y = position.y - sizePx / 2f
        val degrees = ((atan2(x, -y) * 180f / PI.toFloat()) + 360f) % 360f
        if (selectingMinutes) {
            val m = (degrees / 6f).roundToInt() % 60
            if (m != minute) { haptic(ExpressiveHaptic.Tick); currentOnChange(hour, m) }
        } else {
            val k = (degrees / 30f).roundToInt() % 12
            val h = k + if (pm) 12 else 0
            if (h != hour) { haptic(ExpressiveHaptic.Tick); currentOnChange(h, minute) }
        }
    }

    Canvas(
        modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .clip(CircleShape)
            .semantics {
                contentDescription = if (selectingMinutes) "Minute, $minute" else "Hour, ${if (hour % 12 == 0) 12 else hour % 12}"
            }
            .pointerInput(selectingMinutes, hour, minute) {
                detectTapGestures { p ->
                    pick(p, size.width.toFloat())
                    if (!selectingMinutes) currentHourPicked()
                }
            }
            .pointerInput(selectingMinutes, hour, minute) {
                detectDragGestures(
                    onDragStart = { p -> dragging = true; pick(p, size.width.toFloat()) },
                    onDragEnd = { dragging = false; if (!selectingMinutes) currentHourPicked() },
                    onDragCancel = { dragging = false },
                ) { change, _ -> pick(change.position, size.width.toFloat()) }
            },
    ) {
        val r = size.width / 2f
        val c = Offset(r, r)
        val labelRadius = r * 0.78f
        val knob = 24.dp.toPx()
        drawCircle(face, radius = r, center = c)
        val a = Math.toRadians(angle.value.toDouble())
        val tip = Offset(c.x + labelRadius * sin(a).toFloat(), c.y - labelRadius * cos(a).toFloat())
        drawLine(accent, c, tip, strokeWidth = 2.dp.toPx())
        drawCircle(accent, radius = 4.dp.toPx(), center = c)
        drawCircle(accent, radius = knob, center = tip)
        for (i in 0 until 12) {
            val text = if (selectingMinutes) "%02d".format(i * 5) else (if (i == 0) 12 else i).toString()
            val selected = if (selectingMinutes) minute == i * 5 else hour % 12 == i
            val layout = measurer.measure(text, labelStyle.copy(color = if (selected) onAccent else ink))
            val t = i * 30.0 * PI / 180.0
            val p = Offset(c.x + labelRadius * sin(t).toFloat(), c.y - labelRadius * cos(t).toFloat())
            drawText(layout, topLeft = Offset(p.x - layout.size.width / 2f, p.y - layout.size.height / 2f))
        }
        if (selectingMinutes && minute % 5 != 0) drawCircle(onAccent, radius = 3.dp.toPx(), center = tip)
    }
}
