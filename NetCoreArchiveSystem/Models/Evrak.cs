using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace NetCoreArchiveSystem.Models
{
    public class Evrak
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string KlasorId { get; set; } = string.Empty;

        [Required]
        public string EvrakTipi { get; set; } = string.Empty;

        [Required]
        public string DosyaAdi { get; set; } = string.Empty;

        public DateTime YuklemeTarihi { get; set; } = DateTime.Now;

        [ForeignKey("KlasorId")]
        public Klasor? Klasor { get; set; }
    }
}
