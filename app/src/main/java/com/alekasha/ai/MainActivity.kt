package com.alekasha.ai

import android.app.Activity
import android.os.Bundle
import android.speech.RecognizerIntent
import android.speech.tts.TextToSpeech
import android.content.Intent
import android.widget.*
import java.util.Locale

class MainActivity : Activity(), TextToSpeech.OnInitListener {

    private lateinit var input: EditText
    private lateinit var answer: TextView
    private lateinit var speaker: TextToSpeech

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        speaker = TextToSpeech(this, this)

        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(32, 40, 32, 32)

        val heading = TextView(this)
        heading.text = "आलेकाशा AI"
        heading.textSize = 28f
        layout.addView(heading)

        input = EditText(this)
        input.hint = "अपना सवाल लिखें"
        layout.addView(input)

        val send = Button(this)
        send.text = "जवाब दें"
        layout.addView(send)

        val voice = Button(this)
        voice.text = "🎤 बोलकर पूछें"
        layout.addView(voice)

        answer = TextView(this)
        answer.text = "नमस्ते! मैं Alekasha हूँ।"
        answer.textSize = 18f
        layout.addView(answer)

        send.setOnClickListener {
            val q = input.text.toString().trim()
            answer.text = offlineAnswer(q)
            speaker.speak(answer.text, TextToSpeech.QUEUE_FLUSH, null, "reply")
        }

        voice.setOnClickListener {
            val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
            intent.putExtra(
                RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM
            )
            intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "hi-IN")

            try {
                startActivityForResult(intent, 1)
            } catch (e: Exception) {
                answer.text = "आवाज़ पहचानने की सुविधा उपलब्ध नहीं है।"
            }
        }

        setContentView(layout)
    }

    private fun offlineAnswer(q: String): String {
        return when {
            q.contains("नमस्ते") || q.contains("हेलो") ->
                "नमस्ते! मैं Alekasha AI हूँ।"
            q.contains("नाम") ->
                "मेरा नाम Alekasha AI है।"
            q.contains("समय") ->
                "फोन में अभी समय ${java.text.SimpleDateFormat("hh:mm a", Locale.getDefault()).format(java.util.Date())} है।"
            q.isEmpty() ->
                "पहले अपना सवाल लिखिए या बोलिए।"
            else ->
                "अभी मैं ऑफलाइन हूँ। इस सवाल के लिए इंटरनेट और Gemini की सुविधा जोड़नी होगी।"
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == 1 && resultCode == RESULT_OK) {
            val matches = data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
            if (!matches.isNullOrEmpty()) {
                input.setText(matches[0])
            }
        }
    }

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            speaker.language = Locale("hi", "IN")
        }
    }

    override fun onDestroy() {
        speaker.stop()
        speaker.shutdown()
        super.onDestroy()
    }
}
