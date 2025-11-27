class NovelEvaluationFramework:
    def generate_comprehensive_analysis(self, results: List, problem_set: str):
        """Generate novel evaluation reports inspired by the research paper."""
        
        # Original metrics from your project
        basic_metrics = self._calculate_classification_metrics(results)
        
        # Novel additions inspired by the paper
        progressive_analysis = self._analyze_prompt_progression(results)
        persona_impact_analysis = self._analyze_persona_effectiveness(results)
        cot_reasoning_analysis = self._analyze_reasoning_chain_impact(results)
        cross_language_insights = self._generate_java_specific_insights(results)
        
        # Generate research-quality reports
        self._generate_academic_report(problem_set, {
            "basic_metrics": basic_metrics,
            "progressive_analysis": progressive_analysis, 
            "persona_analysis": persona_impact_analysis,
            "reasoning_analysis": cot_reasoning_analysis,
            "java_insights": cross_language_insights
        })
    
    def _analyze_prompt_progression(self, results: List) -> Dict:
        """Analyze improvement from zero-shot → few-shot → CoT → Persona."""
        progression_data = {}
        
        for stage in PromptStage:
            stage_results = [r for r in results if r.request.strategy == stage.value]
            progression_data[stage.value] = {
                "success_rate": len([r for r in stage_results if r.success]) / len(stage_results),
                "avg_execution_time": sum(r.execution_time for r in stage_results) / len(stage_results),
                "avg_token_count": sum(r.token_count for r in stage_results) / len(stage_results),
                "code_quality_score": self._calculate_code_quality(stage_results)
            }
            
        return progression_data
