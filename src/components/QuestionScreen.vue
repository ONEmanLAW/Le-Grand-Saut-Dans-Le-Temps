<template>
    <div class="question-screen">
      <div class="top-bar">
        <div class="question-progress">{{ currentQuestionIndex + 1 }}/{{ totalQuestions }}</div>
        <div class="timer">{{ timer }}s</div>
      </div>
  
      <div class="question-intitule">{{ currentQuestion.question }}</div>
  
      <div class="answers-grid">
        <button
          v-for="(answer, index) in currentQuestion.answers"
          :key="index"
          :class="['answer', selectedAnswer === index ? (index === currentQuestion.correctIndex ? 'correct' : 'wrong') : '']"
          @click="selectAnswer(index)"
          :disabled="answerSelected"
        >
          {{ answer }}
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  
  // Simuler les questions par thème
  const allQuestions = {
    Musique: [
      { question: 'Qui est connu comme le Roi de la Pop ?', answers: ['Elvis Presley', 'Michael Jackson', 'Prince', 'Freddie Mercury'], correctIndex: 1 },
      { question: 'Quel instrument a 88 touches ?', answers: ['Guitare', 'Piano', 'Saxophone', 'Batterie'], correctIndex: 1 },
      { question: 'Quelle chanteuse a sorti "Hello" ?', answers: ['Beyoncé', 'Adele', 'Rihanna', 'Shakira'], correctIndex: 1 },
      { question: 'Lequel est un style musical ?', answers: ['Rock', 'Bleu', 'Rouge', 'Vert'], correctIndex: 0 },
      { question: 'Quel groupe chante "Bohemian Rhapsody" ?', answers: ['Queen', 'Beatles', 'U2', 'Coldplay'], correctIndex: 0 }
    ],
    Politique: [
      { question: 'Qui est le président actuel des États-Unis ?', answers: ['Donald Trump', 'Joe Biden', 'Barack Obama', 'George W. Bush'], correctIndex: 1 },
      { question: 'En quelle année la France a-t-elle adopté la Constitution de la Cinquième République ?', answers: ['1958', '1945', '1970', '1981'], correctIndex: 0 },
      { question: 'Quel est le nom du Premier ministre du Royaume-Uni ? ', answers: ['David Cameron', 'Boris Johnson', 'Theresa May', 'Gordon Brown'], correctIndex: 1 },
      { question: 'Qui a été le président de la France avant Emmanuel Macron ?', answers: ['François Hollande', 'Nicolas Sarkozy', 'Jacques Chirac', 'Valéry Giscard d\'Estaing'], correctIndex: 0 },
      { question: 'Qui a été le premier président de la République française ?', answers: ['Charles de Gaulle', 'Louis-Napoléon Bonaparte', 'Georges Pompidou', 'François Mitterrand'], correctIndex: 1 }
    ],
    Animaux: [
      { question: 'Quel est l’animal terrestre le plus rapide ?', answers: ['Guépard', 'Lion', 'Tigre', 'Éléphant'], correctIndex: 0 },
      { question: 'Quel animal est connu pour sa capacité à changer de couleur ?', answers: ['Caméléon', 'Aigle', 'Serpent', 'Grenouille'], correctIndex: 0 },
      { question: 'Quel est l’animal qui a la plus grande longévité ?', answers: ['Tortue', 'Éléphant', 'Cachalot', 'Pieuvre'], correctIndex: 0 },
      { question: 'Combien de pattes a une araignée ?', answers: ['8', '6', '10', '4'], correctIndex: 0 },
      { question: 'Quel est l’animal qui a le plus grand cerveau par rapport à sa taille ?', answers: ['Dauphin', 'Homme', 'Éléphant', 'Cerveau humain'], correctIndex: 0 }
    ],
    Sport: [
      { question: 'Quel sport se joue avec un ballon rond et des buts ?', answers: ['Football', 'Basketball', 'Tennis', 'Handball'], correctIndex: 0 },
      { question: 'Dans quel sport utilise-t-on un volant ?', answers: ['Badminton', 'Football', 'Basketball', 'Hockey'], correctIndex: 0 },
      { question: 'Quel pays a remporté la Coupe du Monde de la FIFA en 2018 ?', answers: ['Allemagne', 'Brésil', 'France', 'Argentine'], correctIndex: 2 },
      { question: 'Quel est le record du monde du 100 mètres pour hommes ?', answers: ['9.58 secondes', '9.85 secondes', '10.02 secondes', '10.55 secondes'], correctIndex: 0 },
      { question: 'Combien de joueurs y a-t-il dans une équipe de basketball ?', answers: ['5', '7', '6', '10'], correctIndex: 0 }
    ]
  }
  
  // Thèmes disponibles
  const allThemes = ['Musique', 'Politique', 'Animaux', 'Sport']
  
  // Props venant d'App.vue
  const props = defineProps({
    selectedTheme: { type: String, required: true },
    selectedQuestionCount: { type: Number, required: true }
  })
  
  // États
  const questions = ref([])
  const currentQuestionIndex = ref(0)
  const currentQuestion = ref({})
  const selectedAnswer = ref(null)
  const answerSelected = ref(false)
  const timer = ref(60)
  const totalQuestions = ref(0)
  let countdown = null
  
  // Sélectionner les questions selon le thème et le nombre
  onMounted(() => {
    questions.value = allQuestions[props.selectedTheme]
    totalQuestions.value = Math.min(props.selectedQuestionCount, questions.value.length)
    currentQuestion.value = questions.value[currentQuestionIndex.value]
    startTimer()
  })
  
  // Timer
  function startTimer() {
    countdown = setInterval(() => {
      timer.value--
      if (timer.value <= 0) {
        clearInterval(countdown)
        showCorrectAnswer()
      }
    }, 1000)
  }
  
  function selectAnswer(index) {
    if (answerSelected.value) return
    selectedAnswer.value = index
    answerSelected.value = true
    clearInterval(countdown)
  
    setTimeout(() => {
      goToNextQuestion()
    }, 5000)
  }
  
  function showCorrectAnswer() {
    answerSelected.value = true
    setTimeout(() => {
      goToNextQuestion()
    }, 5000)
  }
  
  function goToNextQuestion() {
    if (currentQuestionIndex.value < totalQuestions.value - 1) {
      currentQuestionIndex.value++
      currentQuestion.value = questions.value[currentQuestionIndex.value]
      selectedAnswer.value = null
      answerSelected.value = false
      timer.value = 60
      startTimer()
    } else {
      window.location.reload() // Revenir au début
    }
  }
  </script>
  
  <style scoped>
  .question-screen {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    min-height: 100vh;
    padding: 30px;
    background: #f5f5f5;
    position: relative;
  }
  
  .top-bar {
    width: 100%;
    display: flex;
    justify-content: space-between;
    font-size: 24px;
    font-weight: bold;
    color: #333;
  }
  
  .question-progress {
    margin-left: 10px;
  }
  
  .timer {
    margin-right: 10px;
  }
  
  .question-intitule {
    font-size: 32px;
    margin: 20px 0;
    text-align: center;
    color: #333;
  }
  
  .answers-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
    width: 100%;
    max-width: 500px;
  }
  
  .answer {
    font-size: 20px;
    padding: 20px;
    background-color: #fff;
    border: 2px solid #ccc;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .answer:hover {
    background-color: #f0f0f0;
  }
  
  .correct {
    background-color: #4caf50;
  }
  
  .wrong {
    background-color: #f44336;
  }
  </style>
  