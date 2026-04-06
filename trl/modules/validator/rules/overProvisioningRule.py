
from trl.core.base import ValidationRule, RuleCategory, RuleSeverity
from trl.modules.optimizer.utils.resources import cpu_to_millicores, memory_to_mi 

class OverProvisioningRule(ValidationRule):
     name = "over-provisioning" 
     category = RuleCategory.COST.value
     severity = RuleSeverity.LOW.value

     CPU_THRESHOLD = 1000 # 1 core 
     MEMORY_THRESHOLD = 1024 # 1 Gi 
     
     def match(self, ir): 
        return hasattr(ir, "resources") 
     
     def condition(self, ir): 
        requests = ir.resources.get("requests", {}) 
        limits = ir.resources.get("limits", {}) 
        cpu = requests.get("cpu") 
        memory = requests.get("memory") 
        
        if not cpu and not memory:
             return False 
        
        cpu_mc = cpu_to_millicores(cpu) if cpu else 0 
        mem_mb = memory_to_mi(memory) if memory else 0 
        high_cpu = cpu_mc >= self.CPU_THRESHOLD 
        high_mem = mem_mb > self.MEMORY_THRESHOLD 
        low_replicas = (ir.replicas is None or ir.replicas <= 2) # no burst flexibility 
        
        return (high_cpu or high_mem) and low_replicas
     
     def validate(self, ir, ctx):
        
        ctx.report.warning( 
            category=self.category,
            severity=self.severity, 
            engine = self.engine,
            rule=self.name, 
            resource=ir.name, 
            issue="Resource requests are high relative to workload",
            impact="May lead to inefficient resource utilization and increased cost",
            fix="Reduce resource requests or increase replicas to better distribute workload"
            )