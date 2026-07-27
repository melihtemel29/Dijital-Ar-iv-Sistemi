using System.ComponentModel.DataAnnotations;

namespace NetCoreArchiveSystem.Models
{
    public class Klasor
    {
        [Key]
        public string Id { get; set; } = string.Empty;
        
        [Required]
        public string Ad { get; set; } = string.Empty;
        
        public string Grup { get; set; } = string.Empty;
        
        public string ZorunluEvraklar { get; set; } = string.Empty;
        
        public bool BitisTarihiVarMi { get; set; }
    }
}
